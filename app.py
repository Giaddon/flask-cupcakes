"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config["SECRET_KEY"] = "Shhhhh"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)



@app.route("/api/cupcakes")
def list_cupcakes():
    "Returns JSON object containing all cupcakes"
    cupcake_list = Cupcake.query.all()

    serialized_list = [c.serialize() for c in cupcake_list]


    return jsonify(cupcakes=serialized_list)


@app.route("/api/cupcakes/<int:id>")
def inspect_cupcake(id):
    "Returns JSON object containing data about specified cupcake"

    cupcake = Cupcake.query.get_or_404(id)
    serialized_cupcake = cupcake.serialize()

    return jsonify(cupcake=serialized_cupcake)


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():

    flavor = ""
    size = ""
    rating = 0
    image = None


    try:
        flavor = request.json["flavor"]
    except:
        return ("Error with data submission", 400)

    try:
        size = request.json["size"]
    except:
        return ("Error with data submission", 400)

    try:
        rating = request.json["rating"]
    except:
        return ("Error with data submission", 400)

    image = request.json.get("image", None)

    new_cupcake = Cupcake(flavor=flavor, 
                          size=size,
                          rating=rating,
                          image=image) 

    db.session.add(new_cupcake)
    db.session.commit()

    return ( jsonify(cupcake=new_cupcake.serialize()), 201 )