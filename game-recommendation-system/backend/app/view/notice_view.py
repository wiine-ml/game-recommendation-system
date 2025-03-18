from flask_admin.contrib.sqla import ModelView
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class NoticeView(ModelView):
    # 确保 form_args 是一个字典
    form_args = {
        'title': {
            'label': 'Title',
            'validators': [DataRequired()]
        },
        'content': {
            'label': 'Content',
            'validators': [DataRequired()]
        }
    }

    form_extra_fields = {
        'title': StringField('Title', validators=[DataRequired()]),
        'content': TextAreaField('Content', validators=[DataRequired()])
    }

    column_list = ('id', 
                   'avatar', 
                   'username', 
                   'title', 
                   'content', 
                   'date'
                   )
