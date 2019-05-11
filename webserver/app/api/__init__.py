from flask import Blueprint
from flask_cors import CORS

bp = Blueprint('api', __name__)
CORS(bp)

from . import walls, users, climbs, holds, general
