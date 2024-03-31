from sanic import Blueprint

from src.backend.api.camera.CameraView import get_cameras, create_camera, get_camera, put_camera
from src.backend.api.camera.FrameView import get_frames

camera_bp = Blueprint('camera', url_prefix='/camera', strict_slashes=True)
camera_bp.add_route(uri='/list/', methods=['GET'], handler=get_cameras, strict_slashes=True)
camera_bp.add_route(uri='/', methods=['POST'], handler=create_camera, strict_slashes=True)
camera_bp.add_route(uri='/<camera_id:int>', methods=['PUT'], handler=put_camera, strict_slashes=True)
camera_bp.add_route(uri='/<camera_id:int>', methods=['GET'], handler=get_camera, strict_slashes=True)

camera_bp.add_route(uri='/<camera_id:int>/frame', methods=['GET'], handler=get_frames, strict_slashes=True)
