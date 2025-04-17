from .userData import User
from .scriptsModel import Script
from .videoModel import Video
from .insights import Insights
from .channels import Channel

def init_models():
    # Create all tables
    User.create_table()
    Script.create_table()
    Video.create_table()
    Insights.create_table()
    Channel.create_table()

__all__ = ['User', 'Script', 'Video', 'Insights', 'Channel']

