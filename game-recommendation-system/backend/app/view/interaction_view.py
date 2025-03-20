from flask_admin.contrib.sqla import ModelView
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, BooleanField, DateField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_admin.form import ImageUploadField, DatePickerWidget
from werkzeug.security import generate_password_hash
import os

UPLOAD_FOLDER = 'static/uploads'

# Interaction 视图
class InteractionView(ModelView):
    form_columns = [
        'user', 'game', 'clicked', 'subscribed', 'disliked',
        'review_score', 'review_text', 'created_at'
    ]
    
    form_ajax_refs = {
        'user': {
            'fields': ['username', 'email'],
            'page_size': 10
        },
        'game': {
            'fields': ['gameTitle'],
            'page_size': 10
        }
    }

    form_args = {
        'review_score': {'validators': [Optional()]}
    }
