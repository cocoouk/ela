{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.flask
    pkgs.python311Packages.pymongo
    pkgs.python311Packages.openai
    pkgs.python311Packages.google-auth
    pkgs.python311Packages.google-auth-oauthlib
    pkgs.python311Packages.google-auth-httplib2
    pkgs.python311Packages.google-api-python-client
    pkgs.python311Packages.gspread
    pkgs.python311Packages.notion-client
    pkgs.python311Packages.python-dotenv
    pkgs.python311Packages.flask-limiter
    pkgs.python311Packages.flask-wtf
    pkgs.python311Packages.authlib
    pkgs.python311Packages.structlog
    pkgs.python311Packages.tenacity
  ];
}