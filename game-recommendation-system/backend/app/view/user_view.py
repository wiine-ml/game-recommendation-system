from flask_admin.contrib.sqla import ModelView
from wtforms import StringField, PasswordField, FileField, EmailField
from wtforms.validators import DataRequired, Email, Length
from flask_admin.form import ImageUploadField
from werkzeug.security import generate_password_hash

class UserView(ModelView):
    # 创建和编辑表单中使用的字段
    form_columns = ('email', 'username', 'password', 'avatar')

    # 自定义表单字段
    form_extra_fields = {
        'email': EmailField('email', validators=[DataRequired(), Length(min=2)]),
        'password': PasswordField('Password', validators=[DataRequired(), Length(min=6)]),
        'avatar': ImageUploadField('Avatar', base_path='static/images/avatars', validators=[DataRequired()])
    }

    # 验证规则
    form_args = {
        'email': {
            'label': 'Email',
            'validators': [DataRequired(), Email()]
        },
        'username': {
            'label': 'Username',
            'validators': [DataRequired(), Length(min=2, max=64)]
        }
    }

     # 在创建和编辑用户时自动处理密码哈希
    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = generate_password_hash(form.password.data).decode('utf-8')

    # 在删除用户时清理相关资源（可选）
    def on_model_delete(self, model):
        # 如果需要在删除用户时清理头像文件，可以在这里实现
        pass