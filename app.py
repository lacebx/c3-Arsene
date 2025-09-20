import json
import os
import re
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Optional, List, Dict

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask 
app = Flask(__name__)
CORS(app)

# Load up curated data
def load_curated_data():
    """Load curated data from JSON file."""
    try:
        with open('curated_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning("curated_data.json not found. Using empty dataset.")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing curated_data.json: {e}")
        return []

# Load data
docs = load_curated_data()

# Hard coded response for common user prompts(for fast response)
GREETING_RESPONSES = {
    'hi': 'Hello! How can I help you today?',
    'who are you': "I'm Lace, your virtual assistant.",
    'how are you': "I'm doing well, thank you! How can I help you?",
    'thanks': "You're welcome!",
    'goodbye': 'Goodbye! Have a great day!',
    'bye': 'Goodbye! Take care!',
}

def normalize_query(query: str) -> str:
    """Normalize query for matching."""
    return re.sub(r'[^\w\s]', '', query.lower().strip())

def get_greeting_response(query: str) -> Optional[str]:
    """Check if query matches any greeting patterns."""
    normalized = normalize_query(query)
    
    # Direct match
    if normalized in GREETING_RESPONSES:
        return GREETING_RESPONSES[normalized]
    
    # Pattern matching for variations of user prompts
    greeting_patterns = [
        (r'^(hi|hello|hey|greetings)[\s!.]*$', 'hi'),
        (r'^(what is your name|who are you|tell me about yourself)[\s?]*$', 'what is your name'),
        (r'^(how are you|how do you do|what\'s up|status)[\s?]*$', 'how are you'),
        (r'^(thanks|thank you)[\s!.]*$', 'thanks'),
        (r'^(goodbye|bye|farewell)[\s!.]*$', 'goodbye')
    ]
    
    for pattern, key in greeting_patterns:
        if re.match(pattern, normalized):
            return GREETING_RESPONSES[key]
    
    return None

def simple_text_search(query: str, documents: List[Dict], k: int = 3) -> List[str]:
    """Simple keyword-based text search."""
    if not documents or not query.strip():
        return []
    
    query_words = set(normalize_query(query).split())
    doc_scores = []
    
    for i, doc in enumerate(documents):
        content = doc.get('content', '').lower()
        content_words = set(re.findall(r'\b\w+\b', content))
        
        # Calculate simple keyword overlap score
        overlap = len(query_words.intersection(content_words))
        if overlap > 0:
            doc_scores.append((overlap, i, doc['content']))
    
    # Sort by score (descending) and return k nearest documents
    doc_scores.sort(key=lambda x: x[0], reverse=True)
    return [doc[2] for doc in doc_scores[:k]]

def log_interaction(query: str, response: str):
    """Log user query and bot response to file."""
    try:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "query": query,
            "response": response
        }
        
        with open('logs/interactions.json', 'a') as log_file:
            log_file.write(json.dumps(log_entry) + '\n')
            
    except Exception as e:
        logging.error(f"Error logging interaction: {e}")

def generate_response(query: str) -> str:
    """Generate response based on query."""
    # Check for greeting first
    greeting_response = get_greeting_response(query)
    if greeting_response:
        return greeting_response
    
    # Perform simple text search
    relevant_docs = simple_text_search(query, docs, k=3)
    
    if relevant_docs:
        # Simple response based on retrieved documents
        return f"Based on the available information: {relevant_docs[0][:200]}..."
    else:
        return "I'm not sure how to help with that. Could you please rephrase your question?"

@app.route("/", methods=["GET"])
def home():
    """Health check endpoint."""
    return "Hello, world! I'm running."

@app.route("/chat", methods=["POST"])
def chat():
    """Chat endpoint that processes user queries."""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Empty request body"}), 400
        
        query = data.get("query", "").strip()
        if not query:
            return jsonify({"error": "Query field is required"}), 400
        
        # Generate response
        response = generate_response(query)
        
        # Log interaction
        log_interaction(query, response)
        
        return jsonify({"response": response})
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
