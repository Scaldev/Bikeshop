from flask import Flask, request, abort, render_template
import os
from api.backend import *

TEMPLATES = "templates"

app = Flask(__name__, template_folder=TEMPLATES)

@app.route("/")
@app.route("/home")
def hello():
    print(app.template_folder)
    return render_template("index.html")

@app.route('/<path:page_name>')
def show_page(page_name):
    file_absolution_path = os.path.join("app", TEMPLATES, page_name)
    if not os.path.exists(file_absolution_path):
        print("404", file_absolution_path)
        abort(404)
    return page_manager(page_name)

# cc

def page_manager(page_name):
    file_relative_path   = os.path.join(page_name)
    if page_name == "tout.html":
        return render_template(file_relative_path, tout=get_models())
    if page_name == "dispos.html":
        return render_template(file_relative_path, dispos=get_available_bikes())
    if page_name == "velo.html":
        code = request.args.get('c', default = "", type = str)
        return render_template(file_relative_path, velo_data=get_bike(code), est_dispo=get_available(code))
