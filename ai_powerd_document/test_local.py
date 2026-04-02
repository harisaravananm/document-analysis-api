"""
Quick test script — run this locally before deploying.
Usage: python test_local.py
Requires the API to be running at localhost:8000
"""
import base64
import json
import requests

BASE_URL = "http://localhost:8000"
API_KEY = "sk_track2_987654321"
HEADERS = {"Content-Type": "application/json", "x-api-key": API_KEY}


def encode_file(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def test(file_path: str, file_type: str):
    print(f"\n{'='*50}")
    print(f"Testing: {file_path} [{file_type}]")
    payload = {
        "fileName": file_path.split("/")[-1],
        "fileType": file_type,
        "fileBase64": encode_file(file_path)
    }
    r = requests.post(f"{BASE_URL}/api/document-analyze", headers=HEADERS, json=payload)
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))


def test_unauthorized():
    print(f"\n{'='*50}")
    print("Testing: 401 Unauthorized")
    r = requests.post(f"{BASE_URL}/api/document-analyze",
                      headers={"Content-Type": "application/json", "x-api-key": "wrong_key"},
                      json={"fileName": "test.pdf", "fileType": "pdf", "fileBase64": "abc"})
    print(f"Status: {r.status_code} (expected 401)")


if __name__ == "__main__":
    # Update these paths to match your local sample files
    test("sample1-Technology_Industry_Analysis.pdf", "pdf")
    test("sample2-Cybersecurity_Incident_Report.docx", "docx")
    test("sample3.jpg", "image")
    test_unauthorized()
