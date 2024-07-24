from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, FileField , SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Email,Length, EqualTo, ValidationError
from ..models.user import User 
from flask_login import login_required, current_user
from flask_wtf.file import FileField, FileAllowed

class ItemUploadForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    item_name = StringField('Item Name', validators=[DataRequired()])
    item_category = SelectField('Item Category', choices=[
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('documents', 'Documents'),
        ('miscellaneous', 'Miscellaneous')
    ], validators=[DataRequired()])
    item_color = StringField('Item Color', validators=[DataRequired()])
    item_brand = StringField('Item Brand')
    date_lost_found = DateField('Date Lost/Found', validators=[DataRequired()])
    location_lost_found = StringField('Location Lost/Found', validators=[DataRequired()])
    image = FileField('Item Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Lost', 'Lost'), ('Found', 'Found')], validators=[DataRequired()])
    status = SelectField('Status', choices=[('Lost', 'Lost'), ('Found', 'Found')], validators=[DataRequired()])
    submit = SubmitField('Submit Request')    
    
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    #role_id = SelectField('Role', coerce=int, validators=[DataRequired()]) #bug to save role id
    submit = SubmitField('Sign Up')

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
        
class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')