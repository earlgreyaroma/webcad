from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length

# Create User Form
class UserForm(FlaskForm):
    user_id = StringField(validators=[DataRequired()])
    submit = SubmitField('Start')

# Create Admin Form
class AdminForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Login')

# Create Admin Registration Form
class AdminRegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), EqualTo('password2', message='Passwords Must Match!')])
    password2 = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Register')

# Create Admin Settings Form
class DidForm(FlaskForm):
    did = SelectField(choices=[], validators=[DataRequired()])
    submit_did = SubmitField('Save Document')

# Create Admin Settings Form
class EidForm(FlaskForm):
    eid = SelectField(choices=[], validators=[DataRequired()])
    submit_eid = SubmitField('Save Element')

# Create API Keys Form
class KeysForm(FlaskForm):
    access_key = StringField(validators=[DataRequired()])
    secret_key = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Set Keys')

# Create Test Form
class TestForm(FlaskForm):
    submit = SubmitField('Test')