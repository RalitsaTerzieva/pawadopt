import os
from forms import AddForm, DelForm, AddOwner
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
    owner = db.relationship('Owner', backref='puppy', uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Puppy name is {self.name}"
    
class Owner(db.Model):

    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id

    def __repr__(self):
        return f"Owner with {self.name} has puppy!"

#Views part
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods=["GET", "POST"])
def add_pup():
    form = AddForm()

    if form.validate_on_submit():

        name = form.name.data

        new_puppy = Puppy(name)
        db.session.add(new_puppy)
        db.session.commit()

        return redirect(url_for('list_pup'))

    return render_template('add.html', form=form)

@app.route('/list')
def list_pup():
   
   puppies = Puppy.query.all()
   return render_template('list.html', puppies=puppies)

@app.route('/owner')
def add_owner():
    form = AddOwner()

    if form.validate_on_submit():
        name = form.name.data
        id = form.id.data

        puppy_for_adoption = db.session.get(Puppy, id)
        owner = Owner(name, puppy_id=puppy_for_adoption)

        db.session.add_all([puppy_for_adoption, owner])
        db.session.commit()

    return render_template('owner.html', form=form)

@app.route('/delete', methods=["GET", "POST"])
def delete_pup():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        puppy = Puppy.query.get(id)
        db.session.delete(puppy)
        db.session.commit()

        return redirect(url_for('list_pup'))
    
    return render_template('delete.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)