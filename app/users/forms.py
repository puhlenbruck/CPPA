from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required

class LoginForm(Form):
	username = TextField('username', validators = [Required()])
	password = PasswordField('password', validators = [Required()])


class RegisterForm(Form):
    username = TextField('username', validators = [Required()])
	password = PasswordField('password', validators = [Required()])
	password_confirm = PasswordField('password', validators = [Required()])
	
