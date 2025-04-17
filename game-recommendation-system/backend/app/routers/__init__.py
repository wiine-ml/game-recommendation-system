#file: app/routers/__init__.py
#该文件向app提供蓝图

from .test import test_bp
from .login import login_bp
from .register import register_bp
from .notice import notice_bp
from .game import game_bp
from .game_img import game_img_bp
from .news import news_bp
from .review import review_bp
from .interaction import interaction_bp
from .recommendation import recommendation_bp
from .user import user_bp
from .administrator import administrator_bp
from .autocomplete_search import autocomplete_bp
from .vendor_img import vendor_home_page_bp
from .game_vendor import game_vendor_bp
from .mail import mail_bp