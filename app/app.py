from flask import Flask, request, abort, render_template
import os
from api.main import *
import datetime

import datetime

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
    return render_template("home.html")

@app.route('/tout')
def tout():
    is_page_found("tout")
    bikes = BikeManager.get_bikes()
    print(bikes)
    dispos = BikeManager.get_available_bikes()
    print(dispos)
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
        is_available = BikeManager.is_available(code)
        return render_template("achat.html", code=code, is_available=is_available)
    
    elif request.method == "POST":

        form = request.form
        date = datetime.datetime.today().strftime("%m/%d/%Y, %H:%M:%S")
        
        has_worked = BikeManager.transaction(form, date)

        # Envoyer une réponse
        code = form.get('code')
        bike_data = BikeManager.get_bike_data(code)
        return render_template("confirmation.html", form=form, bike_data=bike_data, date=date, code=code)