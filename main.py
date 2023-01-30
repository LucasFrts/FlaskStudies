from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from os import environ, path
from dotenv import load_dotenv

# Set path to .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

app = Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = str(environ.get('DATABASE'))
# Secret key
app.config['SECRET_KEY'] = str(environ.get('SECRET_KEY'))
# Initialize the database
db = SQLAlchemy(app)

# Create Model
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name


# Create a Form Class
class NameForm(FlaskForm):
    name =  StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField('Submit')
class UserForm(FlaskForm):
    name =  StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField('Submit')



@app.route('/user/add', methods = ['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('User Added Successfully')
    our_users = users.query.order_by(users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)

@app.route('/')
def index():
    favorite_pizza = ["Pepperoni", "Cheese", "Mushorons", 41]
    return render_template("home.html", title="Home", favorite_pizza=favorite_pizza)

@app.route('/user/<name>')
def profile(name):
    return render_template("profile.html", title="Profile", name=name)

@app.route('/name', methods = ['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    # Validate Form
    if form.validate_on_submit():
       name = form.name.data
       form.name.data = '' 
       flash("Form Submitted Sucessfully")

    return render_template('name.html',
    title="Name",
    name = name,
    form = form)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500



if __name__ == '__main__':
    port = int(environ.get("PORT", 9002))
    app.run(debug=True, host="0.0.0.0", port=port)