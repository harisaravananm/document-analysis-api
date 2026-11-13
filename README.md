# Document Analysis API

[![Last commit](https://img.shields.io/github/last-commit/harisaravananm/document-analysis-api?style=for-the-badge)](https://github.com/harisaravananm/document-analysis-api/commits/main)

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
