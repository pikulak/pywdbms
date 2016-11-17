from wtforms import Form, StringField, PasswordField, IntegerField, SelectField, validators
from pywdbms.db.containers import DatabaseContainer
class DatabaseAddForm(Form):
	shortname = StringField('shortname', [validators.Length(min=4, max=20), validators.required()])
	host = StringField('host', [validators.Length(min=4, max=30), validators.required()])
	port = IntegerField('host', [validators.NumberRange(max=65535), validators.required()])
	drivername = SelectField('select_drivername',
							 [validators.Length(min=4, max=30),
							  validators.required()],
							  choices=[('postgresql+psycopg2',
							  		    'postgresql+psycopg2')])

	username = StringField('username', [validators.Length(max=30)])
	password = PasswordField('password', [validators.DataRequired()])
	database = StringField('database', [validators.Length(max=30)])

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False

		if DatabaseContainer.get(self.shortname.data):
			self.shortname.errors.append("Shortname exists")
			return False
		return True