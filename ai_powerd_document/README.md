# Document Analysis API

## Description

An intelligent document processing API that extracts, analyses, and summarises content from PDF, DOCX, and image files. Built for Track 2 of the hackathon — uses Google Gemini 1.5 Flash for AI-powered analysis.

## Tech Stack

- **Framework:** FastAPI (Python)
- **AI/LLM:** Google Gemini 1.5 Flash (`google-generativeai`)
- **PDF Extraction:** PyMuPDF (`fitz`)
- **DOCX Extraction:** python-docx
- **OCR (Image):** Tesseract OCR via pytesseract + Pillow
- **Deployment:** Google Cloud Run (Docker)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/harisaravananm/document-analysis-api
   cd document-analysis-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Also install Tesseract OCR system package:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   
   # macOS
   brew install tesseract
   ```

3. **Set environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

4. **Run the application**
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## API Usage

### Endpoint
`POST /api/document-analyze`

### Headers
```
Content-Type: application/json
x-api-key: sk_track2_987654321
```

### Request Body
```json
{
  "fileName": "sample1.pdf",
  "fileType": "pdf",
  "fileBase64": "<base64_encoded_file_content>"
}
```

### Supported fileType values
- `pdf`
- `docx`
- `image` (JPG, PNG)

### Response
```json
{
  "status": "success",
  "fileName": "sample1.pdf",
  "summary": "Concise summary of document content.",
  "entities": {
    "names": ["John Doe"],
    "dates": ["10 March 2026"],
    "organizations": ["ABC Pvt Ltd"],
    "amounts": ["₹10,000"]
  },
  "sentiment": "Neutral"
}
```

### Error Responses
- `401 Unauthorized` — missing or invalid `x-api-key`
- `400 Bad Request` — unsupported file type or invalid base64
- `422 Unprocessable Entity` — text extraction failed
- `500 Internal Server Error` — AI analysis failure

## Approach

### Text Extraction Strategy
- **PDF:** PyMuPDF iterates each page and extracts raw text with layout order preserved
- **DOCX:** python-docx reads paragraph-level text, preserving document structure
- **Image:** Tesseract OCR with default English language model converts image pixels to text

### AI Analysis Strategy
A single Gemini 1.5 Flash call processes the extracted text with a structured prompt that enforces JSON-only output. The prompt requests:
1. **Summary** — 2-3 factual sentences covering the main document topic
2. **Entities** — Named entity extraction across 4 categories (names, dates, organizations, amounts)
3. **Sentiment** — Overall tone classification (Positive / Neutral / Negative)

Using a single API call instead of separate calls per field reduces latency and API quota usage. The response undergoes JSON parsing with markdown fence stripping as a safety fallback.

## Deployment

```bash
# Build and deploy to Cloud Run
gcloud builds submit --tag gcr.io/YOUR_PROJECT/doc-analysis-api
gcloud run deploy doc-analysis-api \
  --image gcr.io/YOUR_PROJECT/doc-analysis-api \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key,API_KEY=sk_track2_987654321
```
