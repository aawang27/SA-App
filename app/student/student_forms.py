from flask_wtf import FlaskForm
from flask_login import current_user
from app import db
import sqlalchemy as sqla

from app.main.models import User, Instructor, Course, Section
from wtforms import StringField, SubmitField, PasswordField, IntegerField, FloatField, BooleanField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from wtforms.widgets import ListWidget, CheckboxInput

class EditStudentProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired('Error, must enter a value')])
    lastname = StringField('Last Name', validators=[DataRequired('Error, must enter a value')])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    gpa = FloatField('GPA', validators=[DataRequired()])
    graduation_date = StringField('Graduation Date', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AddCourseForm(FlaskForm):
    course = QuerySelectField('Course',
                         query_factory= lambda : db.session.scalars(sqla.select(Course)),
                         get_label= lambda c : 'CS{} - {}'.format(c.coursenum, c.title))
    wasSA = BooleanField('Were you an SA?')
    grade = StringField('Grade recieved')
    term = StringField('What term and year did you take this course?', validators=[DataRequired()])
    submit = SubmitField('Add')