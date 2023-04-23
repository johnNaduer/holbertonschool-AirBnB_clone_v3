#!/usr/bin/python3
""" View for Place objects that handles default API actions In the file api/v1/views/places.py """

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
