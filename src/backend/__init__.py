from sanic import Blueprint

from src.backend.api import api_v1

backend_bp = Blueprint.group(api_v1, url_prefix='/', strict_slashes=True)
