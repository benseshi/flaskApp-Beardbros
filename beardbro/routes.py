from flask import render_template,url_for,flash,redirect,request,session
from beardbro import app, db, bcrypt,mail
from beardbro.forms import RegistrationForm,LoginForm,UpdateForm,PostForm,RequestResetForm,ResetPasswordForm
from beardbro.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
import os
import secrets
from beardbro import Mail
from flask_mail import Message
#from beardbro.watchlist import *
#from alpha_vantage.timeseries import TimeSeries
#from alpha_vantage.techindicators import TechIndicators
#from alpha_vantage.sectorperformance import SectorPerformances
#from alpha_vantage.cryptocurrencies import CryptoCurrencies


#import pandas as pd
#from beardbro.content import content




#TOPIC_DICT=content()

@app.route('/')
@app.route('/home')
def home():
    posts= Post.query.all()#shows the posts that are posted by all users
    return render_template("layout.html",posts=posts)#layout.html contains the required data for posts


@app.route('/dashboard')
@login_required#only if the user is logged in it shows else ask for log in
def dashboard():
    return render_template('dashboard.html',title="Dashboard")#set title as dashboard remaining data contains in html file
@app.route('/about')
@login_required
def about():
    return render_template("about.html",title='About',posts=posts)

#registration process goes with this below code
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:#authenticates the user if authenticated sends to home page
        return redirect(url_for('home'))
    form=RegistrationForm()#gives the values of registration form here like email,password,username,cofirm passsword
    if form.validate_on_submit():#if registeration form is validated all the details
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')#hashes the password
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)#gets hashed password instead of just password,email,username and adds to the database
        db.session.add(user)#adds data to the database user gives the above details
        db.session.commit()#commits changes
        flash('your account is created please login','success')#flashes the message
        return redirect(url_for('login'))#redirects to login page
    return render_template('register.html',title='Register',form=form)#for integrating Userform with the form 



#for logging in 
@app.route('/signin',methods=['GET','POST'])#with post method
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()#login form
    if form.validate_on_submit():#validates the user details on submit
        email=User.query.filter_by(email=form.email.data).first()#filters by email to the given email
        if email and bcrypt.check_password_hash(email.password, form.password.data):#checks email and password validation if validates
            login_user(email)#login user of the email
            next_page=request.args.get('next')#if the user click on any pagelike account,about without logging in it redirects to the login page when user logs in it takes the user to same page 
            #which he tried to access the page
            return redirect(next_page) if next_page else redirect(url_for('home'))
            flash('login success','success')#flashes that login is success
            return redirect(url_for('home'))
        else:
            flash('login in unsuccesfull','danger')
    
    return render_template('signin.html',form=form,title='Login')
#logs out the user
@app.route('/logout')

def logout():
    logout_user()#this is a function from flask_login
    return redirect(url_for('home'))


#saving a picture
def save_picture(form_picture):#takes form_picture as argument
    random_hex=secrets.token_hex(8) #instead of saving file name as something it saves random hexa number
    _,file_ext=os.path.splitext(form_picture.filename)#splits the picture to name and extensions,form_picture here is the data that user submit
    picture_fn=random_hex+file_ext#changes picture with random hexacode and file extension
    picture_path=os.path.join(app.root_path,'static/profilepics',picture_fn)#set picture path as so... with picture name
    form_picture.save(picture_path)#form_picture to save the path in picture path
    return picture_fn

#account details
@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form=UpdateForm()
    if form.validate_on_submit():#validates data on submit
        if form.picture.data:#picture data into the 
            picture_file=save_picture(form.picture.data)#save picture is a method that we created above to save the picture
            current_user.image_file=picture_file#user_image file equals to the picture that saved
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()#commit changes if done
        flash('Your account is updated successfully','success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data=current_user.username#to show the present username 
        form.email.data=current_user.email#to show the present email in the update fields

    image_file=url_for('static',filename='profilepics/'+current_user.image_file)#take the image file from the static folder and profilepics folder curent user image file name
    return render_template('account.html',title='Account',image_file=image_file,form=form)

#this methods is used for posts ignore or remove it if u dont need this
@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)#author acts like the foreignkey
        db.session.add(post)#add the post to the database for particular users
        db.session.commit()#commit changes
        flash('Your Post submitted successfully','success')
        return redirect(url_for('home'))
    return render_template('createpost.html',form=form,title='Posts')

def send_reset_email(user):#intakes ther user data like id
    token=user.get_reset_token()#generates token according to the user that requested for password reset
    msg=Message('Password Reset',sender='noreply@toroi.com',recipients=[user.email])#messge shows the purpose of the email and from the sender and the recipient will be the user that requested
    msg.body=f''' To reset password, visit the follow link:
{url_for('reset_token',token=token,_external=True)}

If you did not make the request please ignore this no changes will be made
'''
    mail.send(msg)#this is the main line that sends the mail with the message


@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()#filters the email of the requested user
        send_reset_email(user)#send the mail to the user 
        flash('An email is sent to your mail please check your mail!','info')
        return redirect(url_for('login'))

    return render_template('reset_request.html',title='Reset password',form=form)

@app.route('/reset_password/<token>',methods=['GET','Post'])
def reset_token(token):
    if current_user.is_authenticated:#as usual authentication of user
        return redirect(url_for('home'))
    user=User.verify_reset_token(token)#verifies the reset token that given to the user when the user clicks on it will be sent to password change
    if user is None:#if the user is not validates or clicks the link after given time as for our program it is 30 mins
        flash('invalid user or session expired','warning')
        return redirect(url_for('reset_request'))
    form=ResetPasswordForm()#integrates password reset form
    if form.validate_on_submit():#on clicking the submit button it starts to check
        hashed_password=bcrypt.generate_password_hash(form.password.data)#generating hashed password for the data of the user password 
        user.password=hashed_password#sets the user password i.e hashed password into the user database of the email that user given
        db.session.commit()#commit the changes
        flash('your password is updated')
        return redirect(url_for('login'))

    return render_template('reset_token.html',title='Reset Password',form=form)
@app.route('/post/<int:post_id>')
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('homepost.html',title='post-title',post=post)
#---------below are the error handlers

@app.errorhandler(405)
def error_405(e):
    return render_template('405.html',title='405')

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html',title='404-Not Found')

@app.errorhandler(500)
def error_404(e):
    return render_template('500.html',title='500-Error')

