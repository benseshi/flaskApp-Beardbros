from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField #description  below
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError #description  below
from beardbro.models import User #importing User form form models file
from flask_login import current_user #the current logged in user
from flask_wtf.file import FileField,FileAllowed #the files which are supports to upload 
'''
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField:

StringField: to get the string data as input in the email and username fields, PasswordField: are
for taking string data as in password format(****),and BooleanField: to check true or false
SubmitField:for submit data and for button mode
--------------------------------------------------------------------------------------------
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError 
DataRequired:to make sure no user pass null data,Length:to give min to max of characters 
Email:to take validation as email(@gmail.com),ValidationError:it raises errors for respective fields
EqualTo:to compare to values of password (during login time to check entered password is same or not with password that in database)
'''

class RegistrationForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
	email=StringField('Email',validators=[DataRequired(),Email()])
	password=PasswordField('Password',validators=[DataRequired()])
	confirm_password=PasswordField('confirm password',validators=[DataRequired(),EqualTo('password')])
	submit=SubmitField('Sign Up')
#validates if username is taken if taken slaps error that username already taken
	def validate_username(self,username):
		user=User.query.filter_by(username=username.data).first()#check the data of username with each username data in database
		if user:#if exists same 
			raise ValidationError('username is already taken')
#validates if email is taken if taken slaps error that email is  already taken
	def validate_email(self,email):
		email=User.query.filter_by(email=email.data).first()#check data of email with each emaill data in database
		if email:#if exists same 
			raise ValidationError('email is already taken')
#login field
class LoginForm(FlaskForm):
	email=StringField('Email',validators=[DataRequired(),Email()])#make sure the email fields are not null and email is a valid one
	password=PasswordField('Password',validators=[DataRequired()])#password field
	submit=SubmitField('Login')#submit button
#update username and emails and picture of existing user
class UpdateForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])#give username that you wanted to change
	email=StringField('Email',validators=[DataRequired(),Email()])#give email that u wanted to change
	picture=FileField('Update profile pic',validators=[FileAllowed(['jpg','png'])])#only jpg and png type of files are allowed
#its better to restrict the type of files allowed to be uploaded to avoid XSS CSRF attacks
	submit=SubmitField('Update')

#validate whether the changed username is taken or not
	def  validate_username(self,username):
		if username.data!=current_user.username:
			user=User.query.filter_by(username=username.data).first()#comparing the data with other users in database
			if user:#if exists same 
				raise ValidationError('username taken')#raise error if taken
#validate whether email is valid or not 
	def validate_email(self,email):
		if email.data!=current_user.email:
			email=User.query.filter_by(email=email.data).first()#comparing the data with every email of other users
			if email:#if exists same 
				raise ValidationError("email alreay taken")
#posting the data if u wanted to use it use it else remove this form
class PostForm(FlaskForm):
	title=StringField('Title',validators=[DataRequired()])
	content=TextAreaField('Content',validators=[DataRequired()])
	submit=SubmitField('Post')
#password reset request form 
class RequestResetForm(FlaskForm):
	email=StringField('email',validators=[DataRequired(),Email()])#we need only email to send password reset request
	submit=SubmitField('Request password reset') #submit button
#checks the given email is exits or not if not gives you error that email doesnt exits
	def validate_email(self,email):
		user=User.query.filter_by(email=email.data).first()
		if user is None:#if user doesnt exits
			raise ValidationError('email doesnt exists with the account please create one first')
#if user clicks on the token that we sent via company email about to reset the password you will get below fiels
class ResetPasswordForm(FlaskForm):
	password=PasswordField('password',validators=[DataRequired()])
	confirm_password=PasswordField('confirm password',validators=[DataRequired(),EqualTo('Password')])#checks given password is same or not
	submit=SubmitField('Reset Password')

