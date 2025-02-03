#!/usr/bin/python3
""" Python script for State Routes & views"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
def get_places(city_id):
    """ Get methods for amenitites routes"""
    # get method
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    if request.method == "GET":
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)


    # post method
    elif request.method == "POST":
        try:
            data = request.get_json(force=True)
        except Exception:
            return jsonify({'error': 'Not a JSON'}), 400

        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        user_id = data.get("user_id")
        if user_id is None:
            return "Missing user_id", 400
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        if "name" not in data:
            return jsonify({'error': 'Missing name'}), 400
        data["city_id"] = city_id
        # create new place
        place = place(**data)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"])
def get_place_id(place_id):
    """ Get methods for retriving places objects by id"""
    place = storage.get("Place", place_id)
    if place is None:
        return jsonify({'error': 'place not found'}), 404
    #return jsonify(place.to_dict())

    # DELETE method
    if request.method == "DELETE":
        place.delete()
        storage.save()
        return jsonify({}), 200

    # GET method
    elif request.method == "GET":
        return jsonify(place.to_dict())

    # PUT method
    elif request.method == "PUT":
        try:
            data = request.get_json(force=True)
        except Exception:
            return jsonify({'error': 'Not a JSON'}), 400

        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        keys_ignored = {"id", "created_at", "user_id", "city_id", "updated_at"}
        [setattr(place, k, v) for k, v in data.items() if k not in keys_ignored]
        place.save()
        return jsonify(place.to_dict()), 200
