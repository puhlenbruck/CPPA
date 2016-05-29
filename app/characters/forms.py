from flask_wtf import Form
from wtforms.fields import TextField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Optional

class CharacterForm(Form):
	id = HiddenField('id')

	name = TextField('Name', validators = [DataRequired(message='Character must have a name')], default = 'name')
	role = TextField('Role', validators = [Optional()])

	intelligence = IntegerField('INT', validators = [Optional()], default = 0)
	reflex = IntegerField('REF', validators = [Optional()], default = 0)
	tech = IntegerField('TECH', validators = [Optional()], default = 0)
	cool = IntegerField('COOL', validators = [Optional()], default = 0)
	attractivness = IntegerField('ATTR', validators = [Optional()], default = 0)
	luck = IntegerField('LUCK', validators = [Optional()], default = 0)
	movement_allowance = IntegerField('MA', validators = [Optional()], default = 0)
	body = IntegerField('BODY', validators = [Optional()], default = 0)
	empathy = IntegerField('EMP', validators = [Optional()], default = 0)
