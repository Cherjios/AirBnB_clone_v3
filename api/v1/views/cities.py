#!/usr/bin/python3
"""Objects that handles all defaul RestFul API actions"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage
from models.city import City

model = "City"
parent_model = "State"



