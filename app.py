from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from notion_client import Client
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
db = None
if MONGODB_URI:
    try:
        client = MongoClient(MONGODB_URI)
        db = client.get_database()
        logger.info("Connected to MongoDB")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {str(e)}")
else:
    logger.warning("MONGODB_URI not set. MongoDB functionality will not be available.")

# Notion connection
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
notion = None
if NOTION_TOKEN:
    try:
        notion = Client(auth=NOTION_TOKEN)
        logger.info("Connected to Notion API")
    except Exception as e:
        logger.error(f"Error connecting to Notion API: {str(e)}")
else:
    logger.warning("NOTION_TOKEN not set. Notion API functionality will not be available.")

# Google services connection
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')
drive_service, sheets_service, forms_service = None, None, None
if GOOGLE_CREDENTIALS:
    try:
        creds_dict = json.loads(GOOGLE_CREDENTIALS)
        creds = service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/forms']
        )
        drive_service = build('drive', 'v3', credentials=creds)
        sheets_service = build('sheets', 'v4', credentials=creds)
        forms_service = build('forms', 'v1', credentials=creds)
        logger.info("Connected to Google services")
    except Exception as e:
        logger.error(f"Error connecting to Google services: {str(e)}")
else:
    logger.warning("GOOGLE_CREDENTIALS not set. Google services functionality will not be available.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gdrive')
def gdrive():
    if not drive_service:
        return render_template('error.html', message="Google Drive service not available"), 503
    try:
        results = drive_service.files().list(pageSize=10, fields="files(id, name, webViewLink)").execute()
        files = results.get('files', [])
        return render_template('gdrive.html', files=files)
    except Exception as e:
        logger.error(f"Error fetching Google Drive files: {str(e)}")
        return render_template('error.html', message="Failed to fetch Google Drive files"), 500

@app.route('/gdrive_links')
def gdrive_links():
    links = [
        {"name": "File 1", "url": "https://drive.google.com/file1"},
        {"name": "File 2", "url": "https://drive.google.com/file2"}
    ]
    return render_template('gdrive_links.html', gdrive_links=links)

@app.route('/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    user_message = request.form.get('message', '')
    if not user_message:
        return jsonify({"response": "Please enter a message."}), 400
    response = f"You said: {user_message}"
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
