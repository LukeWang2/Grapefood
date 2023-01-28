from flask import Flask, flash, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import radish as r
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import LoginManager, UserMixin
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(150), unique=True, index=True)
    password_hash = db.Column(db.String(150))
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class RegistrationForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password1 = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password1")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me", validators=[DataRequired()])
    submit = SubmitField("Login")


SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/home")
def home():
    return render_template("index.html")
