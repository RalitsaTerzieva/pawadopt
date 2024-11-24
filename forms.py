from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):

    name = StringField('Name of puppy: ')
    submit = SubmitField('Add puppy')

class DelForm(FlaskForm):

    id = IntegerField('Id of a puppy to be remove: ')
    submit = SubmitField('Remove puppy')