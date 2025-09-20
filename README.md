# Simple Flask Chat API

A simplified Flask web server with basic chat functionality for testing core API features.

## Features

- **Health Check**: Simple status endpoint at `/`
- **Chat Endpoint**: POST endpoint at `/chat` for processing queries
- **Hardcoded Responses**: Recognizes common greetings and returns appropriate responses
- **Simple Text Search**: Basic keyword matching against curated data
- **Logging**: Logs all interactions to `logs/interactions.json`
- **Error Handling**: Comprehensive error handling for various failure scenarios

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have a `curated_data.json` file (sample provided)

3. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:8080`

## API Endpoints

### GET /
Health check endpoint that returns "Hello, world! I'm running."

### POST /chat
Processes user queries and returns responses.

**Request Body:**
```json
{
  "query": "your question here"
}
```

**Response:**
```json
{
  "response": "bot response here"
}
```

**Error Responses:**
- `400`: Bad request (invalid JSON, missing query, empty query)
- `404`: Endpoint not found
- `405`: Method not allowed
- `500`: Internal server error

## Testing

Run the test script to verify functionality:
```bash
python test_api.py
```

## Logging

All interactions are logged to `logs/interactions.json` with the following format:
```json
{
  "timestamp": "2024-01-01T12:00:00.000Z",
  "query": "user query",
  "response": "bot response"
}
```

## Greeting Recognition

The system recognizes various greetings and responds appropriately:
- "hi", "hello", "hey", "greetings"
- "what is your name", "who are you"
- "how are you", "what's up"
- "thanks", "thank you"
- "goodbye", "bye", "farewell"

## Text Search

For non-greeting queries, the system performs simple keyword matching against the curated data and returns the most relevant document snippet.
