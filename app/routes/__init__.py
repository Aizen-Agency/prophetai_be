# Route definitions

from .routes_auth import api_login
from .routes_script import api_scripts

def init_routes(app):
    app.register_blueprint(api_login)
    app.register_blueprint(api_scripts)
