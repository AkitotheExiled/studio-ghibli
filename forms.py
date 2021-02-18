from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

class SearchForm(FlaskForm):
    choices = SelectField(choices=["Films", "People", "Species", "Locations", "Vehicles"])
    searchbar = StringField("Find films, people...")
    submit = SubmitField("Search")