from flask import Flask, request, abort, render_template
import os
import api.bikes as API
import datetime

TEMPLATES = "templates"

################################################################################################
#                                             UTILS                                            #
################################################################################################

def is_page_found(page_name: str):
    """
    Throws an error 404 page if the page_name doesn't exist.
    @param page_name the name of a page.
    """
    file_absolution_path = os.path.join("app", TEMPLATES, page_name + ".html")
    print("cc")
    if not os.path.exists(file_absolution_path):
        return abort(404)
    
################################################################################################
#                                            ROUTES                                            #
################################################################################################


#########################################    GENERAL    ########################################

app = Flask(__name__, template_folder=TEMPLATES)

@app.route("/")
@app.route("/home")
def hello():
    """
    The home page.
    """
    return render_template("home.html")

@app.route('/tout')
def tout():
    """
    The catalog page: every known bike is displayed.
    """
    bikes = API.get_catalog()
    bikes_available = API.get_available_bikes()
    return render_template("tout.html",
        bikes = bikes,
        bikes_available = bikes_available,
        amount = len(bikes),
        amount_available = len(bikes_available)
    )

@app.route('/dispos')
def dispos():
    """
    The inventory page: every available bike is displayed.
    """
    bikes_available = API.get_available_bikes()
    return render_template("dispos.html",
        bikes_available = bikes_available,
        amount_available = len(bikes_available)
    )

#########################################      BIKE      #########################################

@app.route('/velo')
def velo():
    """
    The page of a specific bike, with its id specified as a valued attribute.
    """
    bike_id = request.args.get('c', default="", type=str)
    bike_description = API.get_bike_description(bike_id)
    is_available = API.is_in_inventory(bike_id)

    return render_template("velo.html",
        bike_description = bike_description,
        is_available = is_available,
        bike_id = bike_id
    )

@app.route('/achat', methods = ["GET", "POST"])
def achat():

    """
    The page for buying a bike.
    """

    if request.method == "GET":

        bike_id = request.args.get('c', default="", type=str)
        bike_name = API.get_bike_description(bike_id)[0]
        is_available = API.is_in_inventory(bike_id)
        
        return render_template("achat.html",
            bike_id = bike_id,
            bike_name = bike_name,
            is_available = is_available
        )
    
    elif request.method == "POST":

        form = request.form
        date = datetime.datetime.today().strftime("%m/%d/%Y, %H:%M:%S")
        has_worked = API.transaction(form, date)

        if not has_worked:
            return render_template("erreur.html")
        
        bike_id = form.get('bike_id')
        bike_name = API.get_bike_description(bike_id)[0]
        return render_template("confirmation.html", form = form, bike_name = bike_name, date = date)


#########################################    INVENTORY    #########################################

@app.route('/creer')
def creer():
    return render_template("creer.html")

@app.route('/modification')
def modification():
    bike_id = request.args.get('c', default="", type=str)
    data_bike = API.get_bike_description(bike_id)
    does_exists = API.is_in_catalog(bike_id)
    return render_template("modification.html", data_bike=data_bike, existe=does_exists, code=bike_id)


@app.route('/reassort')
def reassort():

    bikes = API.get_catalog()
    dispos = API.get_available_bikes()        
    stock = {}
    exemplaire = 0
    
    for bike in bikes:
        stock[bike[0]] = len(API.get_bike_locations(bike[0]))
        exemplaire += len(API.get_bike_locations(bike[0]))

    code = request.args.get('c', default="", type=str)
    return render_template("reassort.html",
        code = code,
        bikes = bikes,
        dispos = dispos,
        stock = stock,
        exemplaire = exemplaire,
        modele = len(bikes)
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_404.html')