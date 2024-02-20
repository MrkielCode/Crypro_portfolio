from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField
from wtforms.validators import DataRequired, length, Email, EqualTo, InputRequired, ValidationError, NumberRange
from portfolio.models import User

class RegistrationForm(FlaskForm):
    """ it handles the registration and validate it"""
    username = StringField('Username', validators=[DataRequired(), length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.')

class LoginForm(FlaskForm):
    """ it handles the registration and validate it"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class TransactionForm(FlaskForm):
    transaction_type = SelectField('Transaction Type', choices=[('1', 'Buy'), ('2', 'Sell')], validators=[InputRequired()])
    coin = SelectField('Coin',
                       choices=[('bitcoin', 'Bitcoin'),
                                ('ethereum', 'Etheruem'),
                                ('solana', 'Solana'),
                                ('binancecoin', 'Binance Coin'),
                                ('ripple', 'XRP')], validators=[InputRequired()])
    cost = FloatField('Amount', validators=[InputRequired(), NumberRange(min=0.01)])  # Adjust the min value as needed
    quantity = FloatField('Quantity', validators=[InputRequired(), NumberRange(min=0.01)])
