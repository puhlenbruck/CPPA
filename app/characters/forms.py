from flask.ext.wtf import Form
from wtforms.fields import TextField
from wtforms.validators import Required

class CharacterForm(Form):
	name = TextField('name', validators = [Required()])
