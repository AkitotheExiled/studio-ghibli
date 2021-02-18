from flask import Flask, render_template, redirect, url_for, request
from forms import SearchForm
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = 'youwikllebifabskjadfhakjs'
sg_api = {"films": "https://ghibliapi.herokuapp.com/films",
          "people": "https://ghibliapi.herokuapp.com/people",
          "locations": "https://ghibliapi.herokuapp.com/locations",
          "species": "https://ghibliapi.herokuapp.com/species",
          "vehicles": "https://ghibliapi.herokuapp.com/vehicles"}





def replace_str(str, replacement, max_limit=30):
  return str[0:max_limit] + replacement


@app.route('/', methods=["GET","POST"])
def index():

    content = {}
    for key,value  in sg_api.items():
        json_data = requests.get(value).json()
        content[key] = json_data


    form = SearchForm()
    if form.validate_on_submit() and request.methods == "POST":

      return redirect(url_for('searchroute', route=form.choices.data, name=form.searchbar.data))
    return render_template("index.html", content=content, form=form)



@app.route("/<category>/<id>", methods=["GET", "POST"])
def show_item(category, id):
    form = SearchForm()
    if form.validate_on_submit():
      return redirect(url_for('searchroute', route=form.choices.data, name=form.searchbar.data))
    print(category)
    for item in requests.get(sg_api[category]).json():
      if id == item["id"]:
        categories = {"films": "film_item", "people": "people_item", "vehicles": "vehicle_item", "locations": "location_item", "species": "specie_item"}
        template = categories[category] + ".html"
        return render_template(template, item=item, form=form)
    return "Cannot find the film you are looking for!"


@app.route("/<category>/", methods=["GET","POST"])
def show_category(category):
    items = requests.get(sg_api[category]).json()
    form = SearchForm()
    print(category)
    if form.validate_on_submit() and request.methods == "POST":
      return redirect(url_for('searchroute', route=form.choices.data, name=form.searchbar.data))
    return render_template("category.html", category=items, form=form, name=category)

@app.route("/search", methods=["GET", "POST"])
def searchroute():
    form = SearchForm()

    if form.validate_on_submit():
        route, name = form.choices.data, form.searchbar.data
        items = []
        for item in requests.get(sg_api[route.lower()]).json():
            if name.lower() in (item.get("title", "").lower() or item.get("name", "").lower()):
                items.append(item)

        return render_template("category.html", category=items, form=form,name=route.lower())
    return redirect(url_for('searchroute'))



def get_id_from_url(url):
    broken_url = url.split("/")
    return broken_url[-1]


def get_category_from_url(url):
    broken_url = url.split("/")
    return broken_url[-2]

@app.context_processor
def utility_processor():
    def form_url_for_item(url):
        category = get_category_from_url(url)
        id = get_id_from_url(url)
        return url_for('show_item', category=category,id=id)
    return dict(form_url_for_item=form_url_for_item)

@app.context_processor
def utility_processor():
    def get_item(url):

        id = get_id_from_url(url)
        category = get_category_from_url(url)

        json_data = requests.get(sg_api[category]).json()
        for item in json_data:
            if item['id'] == id:
                return item
        return category
    return dict(get_item=get_item)

@app.context_processor
def utility_processor():
    def get_items_related_to_url(url):
        print(url.split("/"))
        id = get_id_from_url(url)
        category = get_category_from_url(url)

        json_data = requests.get(sg_api[category]).json()
        items = []
        for item in json_data:
            if item['id'] == id:
                items.append(item)
        return items
    return dict(get_items_related_to_url=get_items_related_to_url)


