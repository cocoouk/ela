from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/gdrive')
def gdrive():
    return render_template('gdrive.html')

@app.route('/gsheets')
def gsheets():
    return render_template('gsheets.html')

@app.route('/mongodb')
def mongodb():
    return render_template('mongodb.html')

@app.route('/gform_responses')
def gform_responses():
    return render_template('gform_responses.html')

@app.route('/notion_pages')
def notion_pages():
    return render_template('notion_pages.html')

if __name__ == "__main__":
    app.run(debug=True)

