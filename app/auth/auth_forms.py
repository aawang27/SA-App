from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FloatField 
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Email
from wtforms.widgets import ListWidget, CheckboxInput
from flask import redirect
from app.main.models import User, Instructor, Course
from app import db
import sqlalchemy as sqla

def is_unique(field_name):
    if field_name == 'username':
        def _is_unique_username(form, field):
            user = db.session.scalars(sqla.select(User).where(User.username == field.data)).first()
            if user is not None:
                # return redirect('auth.login')
                raise ValidationError(message="There is already an account with that username")
        return _is_unique_username
    elif field_name == 'id':
        def _is_unique_id(form, field):
            user = db.session.scalars(sqla.select(User).where(User.id == field.data)).first()
            if user is not None:
                # return redirect('auth.login')
                raise ValidationError(message="There is already an account with that ID")
        return _is_unique_id
    
class LoginForm(FlaskForm):
    email = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember me?')
    submit = SubmitField('Sign In')

class StudentRegistrationForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired('Error, must enter a value'), Email(), is_unique('username')])
    firstname = StringField('First Name', validators=[DataRequired('Error, must enter a value')])
    lastname = StringField('Last Name', validators=[DataRequired('Error, must enter a value')])
    WPI_id = StringField('WPI ID', validators=[DataRequired('Error, must enter a value'), is_unique('id')])
    courses  = QuerySelectMultipleField('Courses Taken', 
                                        query_factory = lambda : db.session.scalars(sqla.select(Course)),
                                        get_label = lambda theCourse : theCourse.title,
                                        widget=ListWidget(prefix_label=False),
                                        option_widget = CheckboxInput())
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    gpa = FloatField('GPA', validators=[DataRequired()])
    graduation_date = StringField('Graduation Date', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class InstructorRegistrationForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired('Error, must enter a value'), Email(), is_unique('username')])
    firstname = StringField('First Name', validators=[DataRequired('Error, must enter a value')])
    lastname = StringField('Last Name', validators=[DataRequired('Error, must enter a value')])
    WPI_id = StringField('WPI ID', validators=[DataRequired(), is_unique('id')])
    title = StringField('Title', validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')