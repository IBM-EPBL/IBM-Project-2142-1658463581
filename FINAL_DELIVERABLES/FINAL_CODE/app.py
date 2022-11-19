from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from datetime import datetime
from flask_migrate import Migrate
from flask_login import UserMixin
from flask import render_template, url_for, flash, redirect, request,session
from flask_login import login_user, current_user, logout_user, login_required
from api_image import image


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ashish210901@127.0.0.1/users'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'ibm_db_sa://rfs19780:D2Ky156OxjrASE8s@2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud.com:30756/bludb'

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
migrate=Migrate(app,db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    details= db.relationship('detail',backref='admin',lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class detail(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    weight=db.Column(db.Integer,nullable=False)
    height=db.Column(db.Float,nullable=False)
    bmi=db.Column(db.Float,nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    
    def __repr__(self):
        return f"details('{self.weight}', '{self.height}','{self.bmi}')"

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    age = StringField('Age',
                           validators=[DataRequired()])
    weight = StringField('Weight',
                        validators=[DataRequired()])
    height = StringField('Height(In metres)',
                        validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Add')

class ImageForm(FlaskForm):
    image = FileField('Image Upload',
                           validators=[FileAllowed(['jpg','jpeg','png'])])

    submit = SubmitField('Check')



@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful, Please Check Mail and Password')
    return render_template('home.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("User added Successfully")
        return redirect(url_for('login'))
    return render_template("register.html",form=form)
    
	

@app.route("/dashboard",methods=['GET', 'POST'])
def dashboard():
    image_file=url_for('static',filename='pics/'+ current_user.image_file)
    return render_template('dashboard.html', image_file=image_file)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/image")
def image():
    return render_template('image.html')

@app.route("/profile",methods=['GET', 'POST'])
def profile():
    form=ProfileForm()
    if form.validate_on_submit():
        weight=form.weight.data
        height=form.height.data
        x=float(weight)
        y=float(height)
        bmi=x/(y**2)
        bmi=round(bmi,2)
        details=detail(weight=weight, height=height, user_id=current_user.id,bmi=bmi)
        db.session.add(details)
        db.session.commit()
        flash("Your BMI is "+str(bmi))
    return render_template('profile.html',form = form)



if __name__=='__main__':
    app.run(debug=True)