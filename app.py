from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'borkborkiamdog'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# db.drop_all()
db.create_all()

def set_edit_info(form, pet):
  """Sets the information for the edit form"""
  form.name.data = pet.name
  form.species.data = pet.species
  form.photo_url.data = pet.photo_url
  form.age.data = pet.age
  form.notes.data = pet.notes
  return form.name.data, form.species.data, form.photo_url.data, form.age.data, form.notes.data

def get_form_info(form, cls):
  """Sets the cls information for Pet"""
  name = form.name.data
  species = form.species.data
  photo_url = form.photo_url.data 
  photo_url = photo_url if photo_url else "https://images.unsplash.com/photo-1546687813-3fcc1c363a07?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=751&q=80"
  age = form.age.data
  notes = form.notes.data
  return cls(name=name, species=species, photo_url=photo_url, age=age, notes=notes)

@app.route("/")
def home_page():
  pets = Pet.query.all()
  return render_template("index.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def new_pet_form():
  form = AddPetForm()
  if form.validate_on_submit():
    pet = get_form_info(form, Pet)
    db.session.add(pet)
    db.session.commit()
    return redirect("/")
  else:
    return render_template("new_pet_form.html", form=form)

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def display_pet(pet_id):
  pet = Pet.query.get(pet_id)
  form = AddPetForm()

  #Sets the information on the edit for if a GET request is sent
  if request.method == "GET":
    set_edit_info(form, pet)
  
  if form.validate_on_submit():
    pet.name = form.name.data
    pet.species = form.species.data
    photo_url = form.photo_url.data 
    pet.photo_url = photo_url if photo_url else "https://images.unsplash.com/photo-1546687813-3fcc1c363a07?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=751&q=80"
    pet.age = form.age.data
    pet.notes = form.notes.data
    db.session.add(pet)
    db.session.commit()
    return redirect(f"/{pet.id}")
  else:
    return render_template("display_pet.html", pet=pet, form=form)

@app.route("/<int:pet_id>/delete")
def delete_pet(pet_id):
  pet = Pet.query.get(pet_id)
  db.session.delete(pet)
  db.session.commit()
  return redirect("/")