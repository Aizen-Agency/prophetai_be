# Route definitions

from .login.routes_auth import api_login
from .scripts.routes_script import api_scripts
from .save_scripts.routes_save_scripts import save_scripts_bp
from .routes_save_videos import video_bp

def init_routes(app):
    app.register_blueprint(api_login)
    app.register_blueprint(api_scripts)
    app.register_blueprint(save_scripts_bp)
    app.register_blueprint(video_bp)
