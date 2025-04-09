# Route definitions

from .routes_auth import api_login

def init_routes(app):
    app.register_blueprint(api_login)
