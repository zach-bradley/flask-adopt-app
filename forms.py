from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, TextField, SelectField
from wtforms.validators import NumberRange, URL, Optional, InputRequired

class AddPetForm(FlaskForm):
  """Form for adding a pet to the database"""
  name = StringField("Pet Name", validators=[InputRequired(message="Please enter a name")])
  species = SelectField("Species", choices=[("dog", "Dog"), ("cat", "Cat"), ("porcupine", "Porcupine")])
  photo_url = StringField("Photo of Pet", validators=[URL(message="Must be a valid URL"), Optional()])
  age = IntegerField("Age of Pet", validators=[NumberRange(min=0,max=30,message="Must be between 0-30"), Optional()])
  notes = TextField("Notes for Pet")