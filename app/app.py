from flask import Flask, request, abort, render_template
import os
from api.main import *

TEMPLATES = "templates"

app = Flask(__name__, template_folder=TEMPLATES)

# UTILITY

def is_page_found(page_name):
    file_absolution_path = os.path.join("app", TEMPLATES, page_name + ".html")
    if not os.path.exists(file_absolution_path):
        return abort(404)

# ROUTES

@app.route("/")
@app.route("/home")
def hello():
    print(app.template_folder)
    return render_template("index.html")

@app.route('/tout')
def tout():
    is_page_found("tout")
    bikes = BikeManager.get_bikes()
    dispos = BikeManager.get_available_bikes()
    return render_template("tout.html", bikes=bikes, dispos=dispos)

@app.route('/dispos')
def dispos():
    is_page_found("dispos")
    dispos = BikeManager.get_available_bikes()
    return render_template("dispos.html", dispos=dispos)

@app.route('/velo')
def velo():
    is_page_found("velo")
    code = request.args.get('c', default="", type=str)
    bike_data = BikeManager.get_bike_data(code)
    is_available = BikeManager.is_available(code)
    return render_template("velo.html", bike_data=bike_data, is_available=is_available, code=code)

@app.route('/achat', methods = ["GET", "POST"])
def achat():
    
    code = request.args.get('c', default="", type=str)
    if request.method == "GET":
        return render_template("achat.html", code=code)
    
    elif request.method == "POST":
        form = request.form
        # TODO : envoyer les informations au côté API

        # TODO : renvoyer sur une page de confirmation
        dispos = BikeManager.get_available_bikes()
        return render_template("dispos.html", dispos=dispos)