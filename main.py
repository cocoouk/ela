import os
import json
import logging
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from notion_client import Client
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

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

# Notion connection
notion = None
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
if NOTION_TOKEN:
    try:
        notion = Client(auth=NOTION_TOKEN)
        logger.info("Connected to Notion API")
    except Exception as e:
        logger.error(f"Error connecting to Notion API: {str(e)}")

# Google services connection
drive_service = None
sheets_service = None
forms_service = None
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')
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

@app.route('/notion')
def notion_route():
    if not notion:
        return render_template('error.html', message="Notion service not available"), 503
    try:
        response = notion.search(filter={"property": "object", "value": "page"})
        pages = [{"title": page['properties'].get('title', [{}])[0].get('text', {}).get('content', 'Untitled'), 
                  "url": page['url']} for page in response['results']]
        return render_template('notion.html', pages=pages)
    except Exception as e:
        logger.error(f"Error fetching Notion pages: {str(e)}")
        return render_template('error.html', message="Failed to fetch Notion pages"), 500

@app.route('/gforms')
def gforms():
    if not forms_service:
        return render_template('error.html', message="Google Forms service not available"), 503
    # Implement Google Forms logic here
    return render_template('gforms.html')

@app.route('/gsheets')
def gsheets():
    if not sheets_service:
        return render_template('error.html', message="Google Sheets service not available"), 503
    # Implement Google Sheets logic here
    return render_template('gsheets.html')

@app.route('/mongo')
def mongo():
    if not db:
        return render_template('error.html', message="MongoDB service not available"), 503
    # Implement MongoDB logic here
    return render_template('mongo.html')

@app.route('/extensions')
def extensions():
    # Implement extensions logic here
    return render_template('extensions.html')

@app.route('/emails')
def emails():
    # Implement email logic here
    return render_template('emails.html')

@app.route('/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    user_message = request.form.get('message', '')
    # Implement chat logic here
    response = f"You said: {user_message}"
    return jsonify({"response": response})

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
    