import os

from dotenv import load_dotenv
from sanic import HTTPResponse, NotFound, Sanic, file
from sanic.response import empty
from sanic_ext import Extend

from src.backend import backend_bp
from src.shared.RabbitMQBroker import broker


from collections import defaultdict
from typing import Dict, FrozenSet

from sanic import Sanic, response
from sanic.router import Route
from typing import Iterable

def _add_cors_headers(response, methods: Iterable[str]) -> None:
    allow_methods = list(set(methods))
    if "OPTIONS" not in allow_methods:
        allow_methods.append("OPTIONS")
    headers = {
        "Access-Control-Allow-Methods": ",".join(allow_methods),
        "Access-Control-Allow-Origin": "http://127.0.0.1:5173 http://127.0.0.1:8000 http://localhost:8000",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Headers": (
            "origin, content-type, accept, "
            "authorization, x-xsrf-token, x-request-id"
        ),
    }
    response.headers.extend(headers)

def add_cors_headers(request, response):
    if request.method != "OPTIONS":
        methods = [method for method in request.route.methods]
        _add_cors_headers(response, methods)


def _compile_routes_needing_options(
    routes: Dict[str, Route]
) -> Dict[str, FrozenSet]:
    needs_options = defaultdict(list)
    # This is 21.12 and later. You will need to change this for older versions.
    for route in routes.values():
        if "OPTIONS" not in route.methods:
            needs_options[route.uri].extend(route.methods)

    return {
        uri: frozenset(methods) for uri, methods in dict(needs_options).items()
    }

def _options_wrapper(handler, methods):
    def wrapped_handler(request, *args, **kwargs):
        nonlocal methods
        return handler(request, methods)

    return wrapped_handler

async def options_handler(request, methods) -> response.HTTPResponse:
    resp = response.empty()
    _add_cors_headers(resp, methods)
    return resp

def setup_options(app: Sanic, _):
    app.router.reset()
    needs_options = _compile_routes_needing_options(app.router.routes_all)
    for uri, methods in needs_options.items():
        app.add_route(
            _options_wrapper(options_handler, methods),
            uri,
            methods=["OPTIONS"],
        )
    app.router.finalize()

app = Sanic('some', strict_slashes=True)

app.blueprint(backend_bp,)
app.static("/login", "static/login/login.html", name="login")
app.static("/login/", "static/login/", name="login-static-files")
app.register_listener(setup_options, "before_server_start")

# Fill in CORS headers
app.register_middleware(add_cors_headers, "response")

@app.route('/assets/<filename>')
async def assets(request, filename):
    return await file(os.path.join('./src/front/dist/assets', filename))

# Catch-all route for serving React app
@app.route('/<path:path>')
async def serve_app(request, path):
    if not path.startswith('api/') and not path.startswith('static/'):
        if path == "login":
            return 
        return await file('./src/front/dist/index.html')
    return HTTPResponse(body="", status=200)


# Optionally, to catch the root and any other path not covered above
@app.route('/')
async def index(request):
    return await file('./src/front/dist/index.html')


Extend(app, cors_config={
    "origins": ["http://127.0.0.1:5173", "http://127.0.0.1:8000", "http://localhost:8000"],
    "allow_methods": ["GET", "POST", "OPTIONS", "PUT", "PATCH"],  # Allow necessary methods
    "allow_headers": ["Content-Type"],  # Allow necessary headers
    "allow_credentials": True,  # Optional, based on your needs
    "expose_headers": [],  # Optional, headers you wish to expose
    "max_age": 600,  # Optional, max age for the OPTIONS preflight cache
})

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


app.config.OAS_CUSTOM_FILE = f'{BASE_DIR}/src/backend/config/schema.yaml'
app.config.secret = "abs" # only for dev

# JWT
app.config.jwt_alg = "HS256"

app.ext.openapi.add_security_scheme(
    "token",
    "http",
    scheme="bearer",
    bearer_format="JWT",
)

@app.get("static/<path:path>")
async def serve_dynamic_file(request, path):
    base_directory = os.path.abspath("./static")  # Ensure this is the correct path to your 'static' directory
    file_path = os.path.join(base_directory, path)

    # Security check: prevent directory traversal attacks
    if not file_path.startswith(base_directory):
        raise NotFound("File not found")

    # Check if the file exists
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise NotFound("File not found")

    return await response.file(file_path)

@app.before_server_start
async def create_broker(app, loop):
    await broker.start()
    app.ctx.broker = broker
    load_dotenv(f'{BASE_DIR}/envs/api.env')
    app.ctx.env = os.getenv




if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True, auto_reload=True, workers=4)


