from database import db
from flask_admin import Admin
from flask import Flask
from config import app_config
from app.view import setup_views

def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config['development'])
    return app

app = create_app()
db.init_app(app)


from app.routers import test_bp, login_bp, register_bp, notice_bp, game_bp, news_bp, interaction_bp, recommendation_bp, review_bp, user_bp, administrator_bp, autocomplete_bp, game_img_bp, vendor_home_page_bp, game_vendor_bp, mail_bp


app.register_blueprint(mail_bp)
app.register_blueprint(user_bp)
app.register_blueprint(test_bp)
app.register_blueprint(news_bp)
app.register_blueprint(game_bp)
app.register_blueprint(login_bp)
app.register_blueprint(review_bp)
app.register_blueprint(notice_bp)
app.register_blueprint(register_bp)
app.register_blueprint(game_img_bp)
app.register_blueprint(interaction_bp)
app.register_blueprint(game_vendor_bp)
app.register_blueprint(autocomplete_bp)
app.register_blueprint(administrator_bp)
app.register_blueprint(vendor_home_page_bp)
app.register_blueprint(recommendation_bp)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
        admin = Admin(app, name='GRS-website', template_mode='bootstrap3')
        setup_views(admin)
        app.run(port=5000, debug=True)
