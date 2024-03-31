from sanic import Blueprint

from src.backend.api.user.UserView import create_user, get_frames_by_user, get_user, get_list_users, delete_user
from src.backend.api.user.auth.TokenView import login_token

auth_token_bp = Blueprint('auth', url_prefix='/auth', strict_slashes=True)
auth_token_bp.add_route(uri='/token', methods=['POST'], handler=login_token, strict_slashes=True)

user_bp = Blueprint('detected_user', url_prefix='/', strict_slashes=True)
user_bp.add_route(uri='/', methods=['POST'], handler=create_user, strict_slashes=True)
user_bp.add_route(uri='/<user_id:int>', methods=['GET'], handler=get_user, strict_slashes=True)
user_bp.add_route(uri='/<user_id:int>', methods=['DELETE'], handler=delete_user, strict_slashes=True)
# user_bp.add_route(uri='/<user_id:int>/last_seen', methods=['GET'], handler="", strict_slashes=True)
user_bp.add_route(uri='/<user_id:int>/frame', methods=['GET'], handler=get_frames_by_user, strict_slashes=True)
user_bp.add_route(uri='/', methods=['GET'], handler=get_list_users, strict_slashes=True)

user_bp_group = Blueprint.group(auth_token_bp, user_bp, url_prefix='/user', strict_slashes=True)
