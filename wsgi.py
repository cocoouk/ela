from main import app

if __name__ != "__main__":
    # This block will be used when running the app with a WSGI server like Gunicorn or Waitress
    application = app

