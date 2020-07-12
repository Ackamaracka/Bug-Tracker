from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    roll = SelectField('Roll', [DataRequired()],
                        choices=[('admin', 'Admin'),
                                 ('manager', 'Manager'),
                                 ('developer', 'Developer')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    roll = SelectField('Roll', 
                        validators=[DataRequired()],
                        choices=[('admin', 'Admin'),
                                 ('manager', 'Manager'),
                                 ('developer', 'Developer')])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ProjectForm(FlaskForm):
    name = StringField('Project Name',
                        validators=[DataRequired()])
    start = DateTimeField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end = DateTimeField('End Date', format='%Y-%m-%d')#, validators=[DataRequired()])
    mngr = SelectField('Manager',
                        validators=[DataRequired()],
                        choices=[('2', 'man2'),
                                 ('1', 'man1'),
                                 ('0', 'man0')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    pr_file = FileField('Project File') 
                        #validators=[FileRequired()]) #FileAllowed(['jpg', 'png'], 'Images only!')
    status = SelectField('Status', 
                        validators=[DataRequired()],
                        choices=[('evaluating', 'Evaluating'),
                                 ('designing', 'Designing'),
                                 ('debugging', 'Debugging'),
                                 ('complete', 'Complete')])
    pitch = TextAreaField('Pitch',
                        validators=[DataRequired()])
    submit = SubmitField('Submit')

class BugForm(FlaskForm):
    name = StringField('Bug Name',
                        validators=[DataRequired()])
    datetime = DateTimeField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    pr_name = SelectField('Project',
                        validators=[DataRequired()],
                        coerce=int)
    frmEmail = StringField('From Email',
                        validators=[DataRequired(), Email()])
    toEmail = StringField('To Email',
                        validators=[DataRequired(), Email()])
    upload = FileField('Bug Screenshot', 
                        validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    prio = SelectField('Priority', 
                        validators=[DataRequired()],
                        choices=[('2', 'High'),
                                 ('1', 'Medium'),
                                 ('0', 'Low')])
    status = SelectField('Status', 
                        validators=[DataRequired()],
                        choices=[('2', 'New'),
                                 ('1', 'Working'),
                                 ('0', 'solved')])
    desc = TextAreaField('Description',
                        validators=[DataRequired()])
    submit = SubmitField('Update')


class ViewProjectForm(FlaskForm):
    name = StringField('Project Name',
                        validators=[DataRequired()])
    pr_file = FileField('image')#, 
                        #validators=[FileRequired()]) #FileAllowed(['jpg', 'png'], 'Images only!')
    status = SelectField('Status', 
                        validators=[DataRequired()],
                        choices=[('evaluating', 'Evaluating'),
                                 ('designing', 'Designing'),
                                 ('debugging', 'Debugging'),
                                 ('complete', 'Complete')])
    pitch = TextAreaField('Pitch',
                        validators=[DataRequired()])
    submit = SubmitField('Update')

class ViewBugForm(FlaskForm):
    name = StringField('Bug Name', 
                        validators=[DataRequired()])
    mngr = SelectField('Manager')
    pr_name = SelectField('Project',
                        validators=[DataRequired()],
                        coerce=int)
    email = StringField('Email')
                        #validators=[DataRequired(), Email()])
    upload = FileField('image') 
                        #validators=[FileRequired(),
                        #FileAllowed(['jpg', 'png'], 'Images only!')])
    prio = SelectField('Priority', 
                        validators=[DataRequired()],
                        choices=[('high', 'High'),
                                 ('medium', 'Medium'),
                                 ('low', 'Low')])
    status = SelectField('Status', 
                        validators=[DataRequired()],
                        choices=[('evaluating', 'Evaluating'),
                                 ('designing', 'Designing'),
                                 ('debugging', 'Debugging'),
                                 ('complete', 'Complete')])
    desc = TextAreaField('Description')
                        #validators=[DataRequired()])
    submit = SubmitField('Update')

class AddUserForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    firstname = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    roll = SelectField('Roll', [DataRequired()],
                        choices=[('admin', 'Admin'),
                                 ('manager', 'Manager'),
                                 ('developer', 'Developer')])
    submit = SubmitField('Add User')


