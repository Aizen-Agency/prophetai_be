from .userData import User
from .scriptsModel import Script
from .videoModel import Video
from .insights import Insights
from .channels import Channel

# Remove automatic table creation on import!

def init_models():
    """
    Call this manually only if you need to create tables (like during initial setup).
    """
    User.create_table()
    Script.create_table()
    Video.create_table()
    Insights.create_table()
    Channel.create_table()

__all__ = ['User', 'Script', 'Video', 'Insights', 'Channel', 'init_models']
