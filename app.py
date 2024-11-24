import os
from forms import AddFrom, DelForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Puppy(db.Model):

    __tablename__ = 'puppies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Puppy name is {self.name}"
    

#Views part
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods=["GET", "POST"])
def add_pup():
    form = AddFrom()

    if form.validate_on_submit():

        name = form.name.data

        new_puppy = Puppy(name)
        db.session.add(new_puppy)
        db.session.commit()

        redirect(url_for('list.html'))

    return render_template('add.html', form=form)