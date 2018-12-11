
from datetime import datetime #import date time 
from toroi import db,login_manager,app #import database from __init__.py 
from flask_login import UserMixin 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #for generating an security token

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#adding data to the database by using this below process
class User(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)#each id given to each user
	username=db.Column(db.String(20),unique=True,nullable=False)#each username to user
	email=db.Column(db.String(120),unique=True,nullable=False)#each mail to user
	password=db.Column(db.String(20),nullable=False)#password field to user
	image_file=db.Column(db.String(20),nullable=False,default='default.jpg')#image file to user and default image will be default.jpg
	posts=db.relationship('Post',backref='author',lazy=True)#this line connects a relationship between the user and posts it acts as a foreignkey
#you can remove this posts line if u not using post form in website im included it if incase
#below line is for generating token which have validation for 30 mins	
	def get_reset_token(self,expires_sec=1800):
		s=Serializer(app.config['SECRET_KEY'],expires_sec)#secret key is what u given for your app
		return s.dumps({'user_id':self.id}).decode('utf-8')#generates token by dumping the user_id of the requested user decode function generates code with no unwanted alphabets

#static method lets the method not to expect any self 
	@staticmethod
	def verify_reset_token(token):#as it takes generated token as argument for verifying
		s=Serializer(app.config['SECRET_KEY'])#secret key is for app validation
		try:
			user_id=s.loads(token)['user_id']#loads the token with user id this user id comes from payload of %return s.dumps({'user_id':self.id}).decode('utf-8')% this line
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):#to reflect username email and image
		return f"User('{self.username}','{self.email}','{self.image_file}')"
#this is the post method to posts the news-feed in home page
class Post(db.Model):
	id=db.Column(db.Integer,primary_key=True)#id is given to the post
	title=db.Column(db.String(100),nullable=False)#title of the post is stored in database
	content=db.Column(db.Text,nullable=False)#content to be stored in database
	date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)#gives date when the post is done
	user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	#binds the post with the user_id that posted with the foreignkey
	def __repr__(self):
		return f"Post('{self.title}','{self.content}','{self.date_posted}','{self.user_id}')"

	