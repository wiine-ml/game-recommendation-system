from flask_admin.contrib.sqla import ModelView
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, BooleanField, DateField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_admin.form import ImageUploadField, DatePickerWidget
from flask_bcrypt import generate_password_hash
import os

UPLOAD_FOLDER = 'static/uploads'
# Developer 视图
class DeveloperView(ModelView):
    form_columns = [
        'DeveloperName', 'DeveloperPassword', 'DeveloperAvatar', 
        'DeveloperProfile', 'DeveloperWebsite', 'DeveloperHeadIllustrations',
        'Address', 'ContactEmail', 'FoundedYear'
    ]
    
    form_extra_fields = {
        'DeveloperPassword': PasswordField('Password', validators=[DataRequired(), Length(min=6)]),
        'DeveloperAvatar': ImageUploadField('Avatar', base_path=os.path.join(UPLOAD_FOLDER, 'developers')),
        'DeveloperHeadIllustrations': ImageUploadField('Head Illustration', base_path=os.path.join(UPLOAD_FOLDER, 'developers'))
    }

    form_args = {
        'DeveloperName': {'validators': [DataRequired()]},
        'ContactEmail': {'validators': [Email()]},
        'FoundedYear': {'validators': [Optional()]}
    }

    def on_model_change(self, form, model, is_created):
        if form.DeveloperPassword.data:
            model.DeveloperPassword = generate_password_hash(form.DeveloperPassword.data)