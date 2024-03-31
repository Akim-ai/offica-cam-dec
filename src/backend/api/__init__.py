from sanic import Blueprint, text

from src.backend.api.camera import camera_bp
from src.backend.api.user import user_bp_group

api_v1 = Blueprint.group(camera_bp, user_bp_group, url_prefix='/api', strict_slashes=True)

