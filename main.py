import os
import json
import logging
from flask import Flask, jsonify, render_template, request
from notion_client import Client
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))  # Use secure secret key

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["500 per day", "100 per hour"],
    storage_uri="memory://"
)

# Notion API connection
notion = None
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
if NOTION_TOKEN:
    try:
        notion = Client(auth=NOTION_TOKEN)
        logger.info("Connected to Notion API")
    except Exception as e:
        logger.error(f"Error connecting to Notion API: {str(e)}")
else:
    logger.error("NOTION_TOKEN not set. Notion API will not be available.")

# Google services connection
drive_service, sheets_service, forms_service = None, None, None
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')

if GOOGLE_CREDENTIALS:
    try:
        creds_dict = json.loads(GOOGLE_CREDENTIALS)
        creds = service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=[
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/forms'
            ]
        )
        drive_service = build('drive', 'v3', credentials=creds)
        sheets_service = build('sheets', 'v4', credentials=creds)
        forms_service = build('forms', 'v1', credentials=creds)
        logger.info("Connected to Google services")
    except json.JSONDecodeError:
        logger.error("Invalid format in GOOGLE_CREDENTIALS environment variable.")
    except Exception as e:
        logger.error(f"Error connecting to Google services: {str(e)}")
else:
    logger.error("GOOGLE_CREDENTIALS not set. Google services will not be available.")

# Routes
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

@app.route('/emails')
def emails():
    return render_template('emails.html')

@app.route('/gsheets')
def gsheets():
    if not sheets_service:
        return render_template('error.html', message="Google Sheets service not available"), 503
    return render_template('gsheets.html')

@app.route('/gform_responses')
def gform_responses():
    if not forms_service:
        return render_template('error.html', message="Google Forms service not available"), 503
    return render_template('gform_responses.html')

@app.route('/notion_pages')
def notion_pages():
    if not notion:
        return render_template('error.html', message="Notion API not available"), 503
    return render_template('notion_pages.html')

@app.route('/extensions')
def extensions():
    return render_template('extensions.html')

# Chat route with rate limiting
@app.route('/chat', methods=['POST'])
@limiter.limit("30 per minute")
def chat():
    user_message = request.form.get('message', '')
    if not user_message:
        return jsonify({"response": "Please enter a message."}), 400
    response = f"You said: {user_message}"
    return jsonify({"response": response})

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

# Error handler for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Error handler for rate limiting
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "Rate limit exceeded", "message": str(e.description)}), 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')


