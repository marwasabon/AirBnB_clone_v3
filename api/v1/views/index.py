#!/usr/bin/python3
"""return the status of your API:"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """Returns the server status."""
    return jsonify({"status": "OK"})


