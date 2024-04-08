from flask import Blueprint, render_template, request,flash, redirect, url_for
from models import User
from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,login_user,logout_user, current_user



#creating a blueprint named auth
auth = Blueprint('auth', __name__)



#creating the login page route in the blueprint auth, this page requires the user to be looged out to access
@auth.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    #if the user fills the email and password field and clicks the login button
    if request.method=='POST':
        email=request.form.get('email')
        passw=request.form.get('passw')
        #checking for user details through the email entered
        user = User.query.filter_by(email=email).first()
        #if the user exists
        if user:
            #and if the password matches, login the user redirecting to the home page
            if check_password_hash(user.passw, passw):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                #flash wrong pw if password doesnt match
                flash('wrong pw!', category="error")
        else:
            #if the user entered doesnt exist
            flash('user doesnt exist!', category="error")
    return render_template("login.html", user= current_user)



#creating the logout route which requires the user to be logged in to access
@auth.route('/logout')
@login_required
def logout():
    #this function logs out the user and redirects to the lgoin page
    logout_user()
    return redirect(url_for("auth.login"))




#creating the route for signup page 
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    #if the user fills the fields and click on sign up 
    if request.method=='POST':
        email=request.form.get('email')
        name=request.form.get('name')
        passw=request.form.get('passw')
        #check if the user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('email exists!', category="error")
        #if the email is too short 
        elif len(email)<4:
            flash('email is too short', category="error")
        #if the name is too short 
        elif len(name)<2:
            flash('name is too short', category="error")
        #if the pw is too short 
        elif len(passw)<7:
            flash('password is too short', category="error")
        #if everything is okay we create a instance of the model User containing the user details and hashed pw
        else:
            new_user = User(email=email,name=name, passw = generate_password_hash(passw, method='pbkdf2:sha256'))
            #add the new_user to the db and commit
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category="success")
            #we login the user and redirect to the home page
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("signup.html", user= current_user)