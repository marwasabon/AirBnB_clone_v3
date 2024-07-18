from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SelectField, TextAreaField, FileField , SubmitField, BooleanField
from wtforms.validators import DataRequired, Email,Length, EqualTo, ValidationError
from ..models.user import User 
from flask_login import login_required, current_user


class ItemUploadForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Lost', 'Lost'), ('Found', 'Found')], validators=[DataRequired()])
    status = SelectField('Status', choices=[('Lost', 'Lost'), ('Found', 'Found')], validators=[DataRequired()])
    image = FileField('Image')
    
    
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    role_id = SelectField('Role', coerce=int, validators=[DataRequired()]) #bug to save role id

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')
        

class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Delete Account')

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('That email is taken. Please choose a different one.')