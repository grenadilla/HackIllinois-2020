from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PurchaseForm(FlaskForm):
    merchant_id = StringField('Merchant ID', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    account = SelectField('Account', choices=[], validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Make Purchase')