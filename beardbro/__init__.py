from flask import Flask #to import flask programs
from flask_sqlalchemy import SQLAlchemy #to get the sqlAlchemy which is also known as database server
from flask_bcrypt import Bcrypt #bcrypt hashing passwords
from flask_login import LoginManager #logging authentication login's
from flask_mail import Mail #import mail authentication



app = Flask(__name__) #app starts from here 
app.config['SECRET_KEY']='c2ba21c063fb53fcbeeb25545181082d' #change this secret key as for your requirement bt key must be compulsary
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db' #this is the database for users email username and hashed_password and imagefiles 
db=SQLAlchemy(app) #this part of the line start integrate sqlalchemy with the app
bcrypt=Bcrypt(app) #bcrypt is called the hashing part of the file to hash to avoid sqlinjectin and xss
login_manager=LoginManager(app) #login functionality to app
login_manager.login_view='login' 
login_manager.login_message_category='info'#the view to let the user to log  in 
#for sending mail to the users about the reset password 
app.config['MAIL_SERVER']='smtp.googlemail.com'#change this service to what u use
app.config['MAIL_PORT']=587 #port number for the service is necessary
app.config['MAIL_USE_TLS']=True #dont change the password
app.config['MAIL_USERNAME']='give email here'#give email here 
app.config['MAIL_PASSWORD']='give password here'#give that email password here
mail=Mail(app)#mail validation mail accessing
#------------------------------------------------------


from beardbro import routes #from here we will be importing routes as a part of program flow
