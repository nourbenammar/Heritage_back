from app import create_app
from app.routes.objects import objects_bp
from app.routes.coloration import coloration_bp
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = create_app()
app.register_blueprint(objects_bp, url_prefix='/objects')
app.register_blueprint(coloration_bp, url_prefix='/coloration')

CORS(app)  # Enable CORS to allow communication with the frontend

API_KEY = 'sec_h7N6A2mxNeIoeW0kAkeV1AwUkHTi1jgY'
PDF_FILE = '/Users/nourbenammar/Desktop/monuments/monuments.pdf'
# Upload and get sourceId once
source_id = None

def upload_pdf():
    """Upload local PDF file to ChatPDF"""
    global source_id
    if source_id:  # Avoid re-uploading if already done
        return source_id

    try:
        with open(PDF_FILE, 'rb') as file:
            files = [('file', (PDF_FILE, file, 'application/octet-stream'))]
            headers = {'x-api-key': API_KEY}
            
            response = requests.post(
                'https://api.chatpdf.com/v1/sources/add-file',
                headers=headers,
                files=files
            )
            
            if response.status_code == 200:
                source_id = response.json()['sourceId']
                return source_id
            else:
                return None
                
    except Exception as e:
        return None

def chat_with_pdf(source_id, question):
    """Interactive chat with PDF"""
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json',
    }

    data = {
        'sourceId': source_id,
        'messages': [{'role': 'user', 'content': question}]
    }
    
    try:
        response = requests.post(
            'https://api.chatpdf.com/v1/chats/message',
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()['content']
        else:
            return f"Error {response.status_code}: {response.text}"
                
    except Exception as e:
        return f"Chat error: {str(e)}"


@app.route('/get-source-id', methods=['GET'])
def get_source_id():
    """Get the source ID for the uploaded PDF"""
    if not source_id:
        return jsonify({'error': 'PDF has not been uploaded yet'}), 400
    return jsonify({'source_id': source_id}), 200


@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint to chat with the uploaded PDF"""
    data = request.get_json()
    
    if not data or 'source_id' not in data or 'question' not in data:
        return jsonify({'error': 'Invalid request, source_id and question are required'}), 400

    source_id = data['source_id']
    question = data['question']
    
    answer = chat_with_pdf(source_id, question)
    
    return jsonify({'answer': answer}), 200


if __name__ == '__main__':
    # Upload PDF once when the server starts (assuming it's already there)
    print(f"Uploading {PDF_FILE}...")
    upload_pdf()
    app.run(debug=True)
