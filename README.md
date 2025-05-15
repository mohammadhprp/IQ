# IQ 🧠

A API-based service that analyzes product comments using AI to provide ratings, summaries, fake comment detection, and keyword extraction.

## Prerequisites

- Docker
- Google API Key for Gemini AI

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mohammadhprp/IQ.git
cd IQ
```

2. Create a `.env` file in the root directory with your Google API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Start the application:

```bash
docker compose up -d
```


The API will be available at `http://localhost:8000`

API Documentation will be available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

2. To stop the application:

```bash
docker compose down
```

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
