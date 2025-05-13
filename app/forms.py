from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField,
    TextAreaField, FileField, SubmitField
)
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 64)])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(6, 128),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Register')

class ProfileForm(FlaskForm):
    username = StringField('New Username', validators=[DataRequired(), Length(3, 64)])
    avatar = FileField('Upload Avatar', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Update Profile')

class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), Length(max=100)])
    body = TextAreaField('Post Body', validators=[DataRequired()])
    submit = SubmitField('Add Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Your Comment', validators=[DataRequired(), Length(max=300)])
    submit = SubmitField('Post Comment')
