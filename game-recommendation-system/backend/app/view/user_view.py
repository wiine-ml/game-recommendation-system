from flask_admin.contrib.sqla import ModelView
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, BooleanField, DateField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_admin.form import ImageUploadField, DatePickerWidget
from werkzeug.security import generate_password_hash
import os

UPLOAD_FOLDER = 'static/uploads'

# User 视图（优化版）
class UserView(ModelView):
    form_columns = ['email', 'username', 'password', 'avatar']
    
    form_extra_fields = {
        'password': PasswordField('Password', validators=[DataRequired(), Length(min=6)]),
        'avatar': ImageUploadField('Avatar', base_path=os.path.join(UPLOAD_FOLDER, 'users'))
    }

    form_args = {
        'email': {'validators': [DataRequired(), Email()]},
        'username': {'validators': [DataRequired(), Length(min=2, max=64)]}
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = generate_password_hash(form.password.data)