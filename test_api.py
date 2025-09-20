#!/usr/bin/env python3
"""
Simple test script for the Flask chat API
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print()

def test_chat_endpoint():
    """Test the chat endpoint with various queries"""
    test_queries = [
        "hi",
        "hello",
        "hey there",
        "what is your name?",
        "how are you?",
        "python programming",
        "machine learning",
        "thanks",
        "goodbye"
    ]
    
    print("Testing chat endpoint...")
    for query in test_queries:
        print(f"Query: '{query}'")
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {data['response']}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 50)

def test_error_handling():
    """Test error handling"""
    print("Testing error handling...")
    
    # Test invalid JSON
    print("Testing invalid JSON...")
    response = requests.post(f"{BASE_URL}/chat", data="invalid json")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print()
    
    # Test empty query
    print("Testing empty query...")
    response = requests.post(f"{BASE_URL}/chat", json={"query": ""})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print()
    
    # Test missing query field
    print("Testing missing query field...")
    response = requests.post(f"{BASE_URL}/chat", json={})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print()

if __name__ == "__main__":
    print("Starting API tests...")
    print("=" * 60)
    
    try:
        test_health_check()
        test_chat_endpoint()
        test_error_handling()
        print("All tests completed!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Flask app is running on port 8080.")
    except Exception as e:
        print(f"Unexpected error: {e}")
