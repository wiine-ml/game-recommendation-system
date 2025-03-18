from flask_admin import Admin
from database import db

from .game_view import GameView
from .news_view import NewsView
from .notice_view import NoticeView
from .user_view import UserView

from ..models import Game, News, Notice, User

def setup_views(admin: Admin):
    admin.add_view(GameView(Game, db.session, name='game'))
    admin.add_view(NewsView(News, db.session, name='news'))
    admin.add_view(NoticeView(Notice, db.session, name='notice'))
    admin.add_view(UserView(User, db.session, name='user'))
    return 

