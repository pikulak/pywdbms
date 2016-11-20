from wtforms import Form, StringField, PasswordField, IntegerField, SelectField, validators
from wtforms.widgets import TextArea
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
        if len(DatabaseContainer.get_databases(host=self.host.data,\
                                               database=self.database.data,\
                                               port=self.port.data)) > 0:
            self.database.errors.append("Database exists")
            return False
        return True

class SqlForm(Form):
    stmt = StringField('stmt', [validators.required()], widget=TextArea())