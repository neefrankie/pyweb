from wtforms import BooleanField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed


class SignUpForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            DataRequired(),
            Length(min=6, max=35),
            Email()
        ],
        description='You email to login'
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(8, 128)
        ]
    )
    confirmPassword = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            Length(8, 128),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[DataRequired(), Length(min=6, max=35), Email()],
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(8, 128)],
    )
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class FileForm(FlaskForm):
    pdf = FileField(
        '',
        validators=[
            FileRequired(),
            FileAllowed(['pdf'])
        ],
        description='Limited only to PDF files'
    )
    submit = SubmitField('Upload')
