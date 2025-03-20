from flask_admin.contrib.sqla import ModelView
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, BooleanField, DateField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_admin.form import ImageUploadField, DatePickerWidget
from flask_bcrypt import generate_password_hash
import os

UPLOAD_FOLDER = 'static/uploads'

# Publisher 视图
class PublisherView(ModelView):
    form_columns = [
        'PublisherName', 'PublisherPassword', 'PublisherAvatar', 
        'PublisherProfile', 'PublisherWebsite', 'PublisherHeadIllstration',
        'Address', 'ContactEmail', 'FoundedYear'
    ]
    
    form_extra_fields = {
        'PublisherPassword': PasswordField('Password', validators=[DataRequired(), Length(min=6)]),
        'PublisherAvatar': ImageUploadField('Avatar', base_path=os.path.join(UPLOAD_FOLDER, 'publishers')),
        'PublisherHeadIllstration': ImageUploadField('Head Illustration', base_path=os.path.join(UPLOAD_FOLDER, 'publishers'))
    }

    def on_model_change(self, form, model, is_created):
        if form.PublisherPassword.data:
            model.PublisherPassword = generate_password_hash(form.PublisherPassword.data)
