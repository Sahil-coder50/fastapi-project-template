from .cors import setup_cors

def setup_middlewares(app):
    setup_cors(app)