from flask import Flask, request, redirect , flash, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError,DataRequired, Length, Email, EqualTo
 
app = Flask(__name__)
app.debug = True
 
# adding configuration for using a sqlite database
app.config['SECRET_KEY'] = '12345678'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
bcrypt =Bcrypt(app)

with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return User('{self.username}', '{self.email}', '{self.image_file}')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

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


@app.route('/',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Logged in successfully','success')
                return 'Dashboard of {user}'
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('home.html', title='Login', form=form)
 
@app.route('/register',methods = ['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created!','success')
        return redirect(url_for('/'))
        # username = request.form.get("username")
        # email = request.form.get("email")
        # password = request.form.get("password")
        # # create an object of the Profile class of models
        # # # and store data as a row in our datatable
        # if username != '' and email != '' and password !='' is not None:
        #     p = User(username=username, email=email, password=password)
        #     db.session.add(p)
        #     db.session.commit()
        #     return redirect('/')
    return render_template('register.html',title='Register',form=form)
    #     hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    #     user = User(username=form.username.data, email=form.email.data,password=hashed_password)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash('Welcome Aboard!!You Can Log In', 'success')
    #     return redirect(url_for('home'))
    # return render_template('register.html', title='Register', form=form)
@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run()