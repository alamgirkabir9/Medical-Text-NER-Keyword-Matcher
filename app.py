from flask import Flask, render_template, request, jsonify, session
import spacy
import json
import requests
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
from spacy.matcher import Matcher
import os
import pandas as pd
from werkzeug.utils import secure_filename
import zipfile
import shutil
import tempfile
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')  # Use environment variable
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variables to store loaded model and matcher
nlp_model = None
matcher_model = None

# Default model configuration
DEFAULT_MODEL_URL = "https://github.com/alamgirkabir9/Medical-Text-NER-Keyword-Matcher/archive/refs/heads/main.zip"
DEFAULT_MODEL_PATH = "saved_model_with_patterns"

def download_and_extract_model(github_url, extract_path="model_temp"):
    """Download and extract model from GitHub repository"""
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "model.zip")
        
        # Download the repository
        print(f"Downloading model from: {github_url}")
        response = requests.get(github_url, stream=True, timeout=300)
        response.raise_for_status()
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Extract the zip file
        extract_dir = os.path.join(temp_dir, "extracted")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find the model directory
        extracted_contents = os.listdir(extract_dir)
        repo_dir = os.path.join(extract_dir, extracted_contents[0])  # First directory
        model_source = os.path.join(repo_dir, "saved_model_with_patterns")
        
        if not os.path.exists(model_source):
            return None, "Model directory not found in the repository"
        
        # Copy to local directory
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)
        shutil.copytree(model_source, extract_path)
        
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        
        return extract_path, "Model downloaded and extracted successfully"
        
    except Exception as e:
        # Clean up on error
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return None, f"Error downloading model: {str(e)}"

def extract_text_from_url(url):
    """Extract text from a website URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def load_model_with_patterns(load_dir):
    """Load spaCy model and matcher patterns"""
    # If load_dir is a URL, download the model first
    if load_dir.startswith(('http://', 'https://')):
        print("Detected URL, downloading model...")
        local_path, message = download_and_extract_model(load_dir)
        if not local_path:
            return None, None, message
        load_dir = local_path
    
    try:
        nlp = spacy.load(load_dir)
        model_info = {
            'name': nlp.meta.get('name', 'Unknown'),
            'version': nlp.meta.get('version', 'Unknown')
        }
    except Exception as e:
        return None, None, f"Error loading model: {str(e)}"

    # Load matcher patterns
    patterns_file = os.path.join(load_dir, "matcher_patterns.json")
    matcher = None
    
    if os.path.exists(patterns_file):
        try:
            with open(patterns_file, "r", encoding="utf-8") as f:
                medical_patterns = json.load(f)
            
            # Initialize the matcher
            matcher = Matcher(nlp.vocab)
            for label, patterns in medical_patterns.items():
                if label not in matcher:
                    for pattern in patterns:
                        matcher.add(label, [pattern])
        except Exception as e:
            return nlp, None, f"Warning: Error loading matcher patterns: {str(e)}"
    
    return nlp, matcher, f"Model loaded successfully: {model_info['name']} (v{model_info['version']})"

def analyze_text(text, nlp, matcher):
    """Analyze text using NLP model and matcher"""
    doc = nlp(text)
    results = []
    
    # Extract Named Entities
    for ent in doc.ents:
        results.append({
            'text': ent.text,
            'label': ent.label_,
            'source': 'NER',
            'start': ent.start_char,
            'end': ent.end_char
        })
    
    # Extract Matcher results
    if matcher:
        matches = matcher(doc)
        for match_id, start, end in matches:
            label = nlp.vocab.strings[match_id]
            span = doc[start:end]
            results.append({
                'text': span.text,
                'label': label,
                'source': 'Matcher',
                'start': span.start_char,
                'end': span.end_char
            })
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_model', methods=['POST'])
def load_model():
    global nlp_model, matcher_model
    
    model_dir = request.json.get('model_dir', DEFAULT_MODEL_URL)
    if not model_dir:
        return jsonify({'success': False, 'message': 'Model directory path is required'})
    
    try:
        nlp_model, matcher_model, message = load_model_with_patterns(model_dir)
        
        if nlp_model:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Unexpected error: {str(e)}'})

@app.route('/extract_url', methods=['POST'])
def extract_url():
    url = request.json.get('url')
    if not url:
        return jsonify({'success': False, 'message': 'URL is required'})
    
    text = extract_text_from_url(url)
    return jsonify({'success': True, 'text': text})

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})
    
    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})
    
    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        text = extract_text_from_pdf(filepath)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({'success': True, 'text': text})
    else:
        return jsonify({'success': False, 'message': 'Please upload a PDF file'})

@app.route('/analyze', methods=['POST'])
def analyze():
    global nlp_model, matcher_model
    
    if not nlp_model:
        return jsonify({'success': False, 'message': 'Please load the model first'})
    
    text = request.json.get('text', '').strip()
    if not text:
        return jsonify({'success': False, 'message': 'No text provided for analysis'})
    
    try:
        results = analyze_text(text, nlp_model, matcher_model)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Analysis error: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)