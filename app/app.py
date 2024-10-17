from flask import Flask, request, abort, render_template
import os
from api.main import *

TEMPLATES = "templates"

app = Flask(__name__, template_folder=TEMPLATES)

@app.route("/")
@app.route("/home")
def hello():
    return render_template("index.html")

@app.route('/<path:page_name>')
def show_page(page_name):
    file_absolution_path = os.path.join("app", TEMPLATES, page_name + ".html")
    if not os.path.exists(file_absolution_path):
        abort(404)
    return page_manager(page_name)

def page_manager(page_name):
    if page_name == "tout":
        return render_template("tout.html", tout = BikeManager.get_bikes())
    if page_name == "dispos":
        return render_template("dispos.html", dispos=BikeManager.get_available_bikes())
    if page_name == "velo":
        code = request.args.get('c', default = "", type = str)
        return render_template("velo.html", velo_data=BikeManager.get_bike_data(code), est_dispo=BikeManager.is_available(code))
