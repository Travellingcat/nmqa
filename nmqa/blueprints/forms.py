import wtforms
from wtforms.validators import length,email,EqualTo,InputRequired
from models import EmailCaptchaModel,UserModel

# 表单验证器
class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    # 增加validate_xxx函数进一步验证表单
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError("邮箱验证码错误！")

    def vaildate_email(self, field):
        email = field.data
        email_model = UserModel.query.filter_by(email=email).first()
        if email_model:
            raise wtforms.ValidationError("该邮箱已注册！")


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=1, max=50)])
    content = wtforms.StringField(validators=[length(min=1)])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])