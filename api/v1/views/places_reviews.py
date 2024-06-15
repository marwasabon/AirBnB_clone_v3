#!/usr/bin/python3
""" Python script for State Routes & views"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.Amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"])
def amenities():
    """ Get methods for amenitites routes"""
    # GET method
    if request.method == "GET":
        return jsonify([a.to_dict() for a in storage.all("Amenity").values()])

    # POST method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if data.get("name") is None:
        return "Missing name", 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"])
def amenity_id(amenity_id):
    """Defines GET, PUT and DELETE methods for a specific ID on /amenities.
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    # GET method defin
    if request.method == "GET":
        return jsonify(amenity.to_dict())

    # DELETE method defin
    elif request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({})

    # PUT method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    avoid = {"id", "created_at", "updated_at"}
    [setattr(amenity, k, v) for k, v in data.items() if k not in avoid]
    amenity.save()
    return jsonify(amenity.to_dict())
