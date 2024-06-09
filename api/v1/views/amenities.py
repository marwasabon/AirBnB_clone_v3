#!/usr/bin/python3
""" Python script for State Routes & views"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"])
def get_amenites():
    """ Get methods for amenitites routes"""
    # get method
    if request.method == "GET":
        amenitites = []
        for amenity in storage.all("Amenity").values():
            amenitites.append(amenity.to_dict())
        return jsonify(amenitites)

    # post method
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "name" not in data:
        return jsonify({'error': 'Missing name'}), 400

    # create new amenity
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"])
def get_amenity_id(amenity_id):
    """ Get methods for retriving amenities objects by id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        return jsonify({'error': 'Amenity not found'}), 404
    return jsonify(amenity.to_dict())

    # DELETE method
    if request.method == "DELETE":
        amenity.delete()
        storage.save()
        return jsonify({}), 200

    # GET method
    elif request.method == "GET":
        return jsonify(amenity.to_dict())

    # PUT method
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    keys_ignored = {"id", "created_at", "updated_at"}
    [setattr(amenity, k, v) for k, v in data.items() if k not in keys_ignored]
    amenity.save()
    return jsonify(amenity.to_dict()), 200
