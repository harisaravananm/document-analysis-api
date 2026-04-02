import os
import base64
import json
import tempfile
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import google.generativeai as genai
import fitz  # PyMuPDF
from docx import Document
import pytesseract
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Document Analysis API", version="1.0.0")

API_KEY = os.getenv("API_KEY", "sk_track2_987654321")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


class DocumentRequest(BaseModel):
    fileName: str
    fileType: str  # pdf / docx / image
    fileBase64: str


class EntitiesResponse(BaseModel):
    names: list[str]
    dates: list[str]
    organizations: list[str]
    amounts: list[str]


class DocumentResponse(BaseModel):
    status: str
    fileName: str
    summary: str
    entities: dict
    sentiment: str


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    doc = Document(tmp_path)
    os.unlink(tmp_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])


def extract_text_from_image(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    img = Image.open(tmp_path)
    text = pytesseract.image_to_string(img)
    os.unlink(tmp_path)
    return text.strip()


def analyze_with_gemini(text: str, file_name: str) -> dict:
    prompt = f"""Analyze the following document content and return ONLY a valid JSON object with no markdown, no code fences, no explanation.

Document: {file_name}
Content:
{text[:4000]}

Return this exact JSON structure:
{{
  "summary": "A concise 2-3 sentence summary of the document.",
  "entities": {{
    "names": ["list of person names found"],
    "dates": ["list of dates found"],
    "organizations": ["list of organization names found"],
    "amounts": ["list of monetary amounts found"]
  }},
  "sentiment": "Positive or Neutral or Negative"
}}

Rules:
- summary: 2-3 sentences, factual, covers main topic
- entities: extract only what's explicitly present; use empty list [] if none found
- sentiment: exactly one of Positive / Neutral / Negative based on overall tone
- Return ONLY the JSON, nothing else"""

    response = model.generate_content(prompt)
    raw = response.text.strip()
    # Strip markdown fences if model adds them
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


@app.get("/")
def root():
    return {"message": "Document Analysis API is running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/document-analyze", response_model=DocumentResponse)
def analyze_document(
    request: DocumentRequest,
    x_api_key: str = Header(None)
):
    # Auth check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API key")

    # Decode base64
    try:
        file_bytes = base64.b64decode(request.fileBase64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 encoded file")

    # Extract text based on type
    file_type = request.fileType.lower()
    try:
        if file_type == "pdf":
            text = extract_text_from_pdf(file_bytes)
        elif file_type == "docx":
            text = extract_text_from_docx(file_bytes)
        elif file_type in ("image", "jpg", "jpeg", "png"):
            text = extract_text_from_image(file_bytes)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported fileType: {request.fileType}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Text extraction failed: {str(e)}")

    if not text:
        raise HTTPException(status_code=422, detail="No text could be extracted from the document")

    # AI analysis
    try:
        result = analyze_with_gemini(text, request.fileName)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI returned malformed JSON, retry")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

    return DocumentResponse(
        status="success",
        fileName=request.fileName,
        summary=result.get("summary", ""),
        entities=result.get("entities", {"names": [], "dates": [], "organizations": [], "amounts": []}),
        sentiment=result.get("sentiment", "Neutral")
    )
