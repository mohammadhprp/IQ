# IQ - Product Analyzer API

A FastAPI-based service that analyzes product comments using AI to provide ratings, summaries, fake comment detection, and keyword extraction.

## Features

- Product rating analysis (1-5 scale)
- Comment summary generation
- Fake comment detection
- Keyword extraction
- RESTful API interface

## Prerequisites

- Python 3.8+
- Google API Key for Gemini AI

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mohammadhprp/IQ.git
cd IQ
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate 
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your Google API key:

```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Start the server:

```bash
python -m app.main
```

2. The API will be available at `http://localhost:8000`

3. API Documentation will be available at:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /api/analyze

Analyzes a product and its comments.

Request body:

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "comments": [
    {
      "id": "string",
      "user_id": "string",
      "text": "string"
    }
  ]
}
```

Response:

```json
{
  "rating": 4.5,
  "summary": "string",
  "fake_comments": ["string"],
  "keywords": ["string"]
}
```
