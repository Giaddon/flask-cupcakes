"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake, DEFAULT_IMG
from sqlalchemy import or_


app = Flask(__name__)

app.config["SECRET_KEY"] = "Shhhhh"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

HTTP_STATUS_CODE_CREATED = 201


@app.route("/")
def homepage():

    return render_template("cupcake_list.html")


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
    """ validates the body of the request; then create a cupcake with data from the request """

    try:
        flavor = request.json["flavor"]
    except KeyError:
        return ("Flavor: wrong input format", 400)

    try:
        size = request.json["size"]
    except KeyError:
        return ("Size: wrong input format", 400)

    try:
        rating = request.json["rating"]
    except KeyError:
        return ("Rating: wrong input format", 400)

    image = request.json.get("image", None)

    new_cupcake = Cupcake(flavor=flavor,
                          size=size,
                          rating=rating,
                          image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), HTTP_STATUS_CODE_CREATED)


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def cupcake_update(id):
    """Upadate a cupcake with PATCH method, return updated JSON """

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json['flavor']
    cupcake.rating = request.json['rating']
    cupcake.size = request.json['size']
    cupcake.image = request.json.get("image", DEFAULT_IMG)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def cupcake_delete(id):
    """Delete cupcake with the id passed in the URL """

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")


@app.route("/api/search/<search_terms>")
def search_cupcakes(search_terms):
    """Query database for cupcakes matching search term,
    respond with JSON of results"""
    
    # Should work with params? 
    # for seperate fields
    search_result = Cupcake.query.filter(or_(Cupcake.flavor.ilike(f"%{search_terms}%"), 
                                        Cupcake.size.ilike(f"%{search_terms}%"))).all()

    if search_result:
        serialized_list = [c.serialize() for c in search_result]
        return jsonify(cupcakes=serialized_list)
    else:
        return "No cupcakes found."
