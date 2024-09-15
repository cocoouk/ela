from flask import Flask, render_template

app = Flask(__name__)

# Route for the frontpage with the chat interface
@app.route('/')
def index():
    return render_template('index.html')

# Route for Google Drive links
@app.route('/gdrive')
def gdrive():
    return render_template('gdrive.html')

# Route for Google Forms responses
@app.route('/gforms')
def gform_responses():
    return render_template('gform_responses.html')

# Route for Google Sheets data
@app.route('/gsheets')
def gsheets():
    return render_template('gsheets.html')

# Route for Notion pages
@app.route('/notion')
def notion_pages():
    return render_template('notion_pages.html')

# Route for MongoDB collections
@app.route('/mongo')
def mongo_collections():
    return render_template('mongodb.html')

# Route for extensions
@app.route('/extensions')
def extensions():
    return render_template('extensions.html')

# Route for emails (currently not implemented)
@app.route('/emails')
def emails():
    return render_template('emails.html')

# Route for the 404 page (custom error page)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
