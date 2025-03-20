from flask_admin import Admin
from database import db

from .game_view import GameView
from .news_view import NewsView
from .notice_view import NoticeView
from .user_view import UserView

from .interaction_view import InteractionView
from .developer_view import DeveloperView
from .publisher_view import PublisherView

from ..models import Game, News, Notice, User, Interaction, Developer, Publisher

def setup_views(admin: Admin):
    admin.add_view(GameView(Game, db.session, name='game'))
    admin.add_view(NewsView(News, db.session, name='news'))
    admin.add_view(NoticeView(Notice, db.session, name='notice'))
    admin.add_view(UserView(User, db.session, name='user'))
    #admin.add_view(InteractionView(Interaction, db.session, name='interaction'))
    admin.add_view(DeveloperView(Developer, db.session, name='developer'))
    admin.add_view(PublisherView(Publisher, db.session, name='publisher'))
    return 

