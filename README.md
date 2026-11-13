# Document Analysis API

<!-- tech-version-badges -->
![FastAPI 0.115.0](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![Python 3.10%2B](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Google GenAI%201.10.0](https://img.shields.io/badge/Google-GenAI%201.10.0-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white) ![PyMuPDF 1.24.11](https://img.shields.io/badge/PyMuPDF-1.24.11-3776AB?style=for-the-badge) ![Tesseract OCR](https://img.shields.io/badge/Tesseract-OCR-5A5A5A?style=for-the-badge)
<!-- /tech-version-badges -->

An AI-powered FastAPI service that analyzes PDF, DOCX, and image documents using Google Gemini. It extracts entities, creates summaries, and classifies sentiment.

## Table of Contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Quick start](#quick-start)
- [Project structure](#project-structure)
- [License](#license)

## Features

- Clear project organization for learning, experimentation, or demonstration
- Project-specific workflows documented below
- Reproducible local setup instructions

## Tech stack

FastAPI, Python, Google Gemini, PyMuPDF, python-docx, Tesseract OCR, Docker

## Quick start

```bash
git clone https://github.com/harisaravananm/document-analysis-api.git
cd document-analysis-api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Install Tesseract OCR for image input, set `GEMINI_API_KEY` and the API key used by the service, then run:

```bash
uvicorn app.main:app --reload --port 8000
```

## Project structure

```text
.
|-- app/
|-- Dockerfile
`-- requirements.txt
```

## License

No root LICENSE file is currently included.