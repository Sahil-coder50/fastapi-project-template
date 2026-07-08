from .exceptions import setup_global_exception, setup_db_exception

def setup_exceptions(app):
    setup_db_exception(app)
    setup_global_exception(app)

__all__ = [
    "setup_exceptions",
    
]