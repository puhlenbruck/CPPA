from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required

class LoginForm(Form):
	username = TextField('username', validators = [Required()], description='username')
	password = PasswordField('password', validators = [Required()], description='password')


class RegisterForm(Form):
    username = TextField('username', validators = [Required()], description='username')
    password = PasswordField('password', validators = [Required()], description='password')
    password_confirm = PasswordField('password', validators = [Required()], description='repeat password')
