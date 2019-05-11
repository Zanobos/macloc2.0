from os import listdir
from os.path import isfile, join
from app import db
from app.api import bp
from app.models import Wall
from app.api.errors import bad_request, unauthorized
from flask import request, jsonify, url_for
from flask import current_app as app

@bp.route('/walls/<int:wallid>', methods=['GET'])
def get_wall(wallid):
    return jsonify(Wall.query.get_or_404(wallid).to_dict())

@bp.route('/walls', methods=['GET'])
def get_walls():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 1000, type=int), 1000)
    data = Wall.to_collection_dict(Wall.query, page, per_page, 'api.get_walls')
    data['active'] = any(wall.active is True for wall in Wall.query.all())
    return jsonify(data)

@bp.route('/walls', methods=['POST'])
def create_wall():
    data = request.get_json() or {}
    if 'width' not in data or 'height' not in data or 'grade' not in data:
        return bad_request('must include width, height and grade')
    wall = Wall()
    data['active'] = False
    wall.from_dict(data)
    db.session.add(wall)
    db.session.commit()
    response = jsonify(wall.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_wall', wallid=wall.id)
    return response

@bp.route('/walls/<int:wallid>', methods=['PUT'])
def update_wall(wallid):
    wall = Wall.query.get_or_404(wallid)
    data = request.get_json() or {}
    wall.from_dict(data)
    db.session.commit()
    return jsonify(wall.to_dict())

@bp.route('/walls/<int:wallid>', methods=['PATCH'])
def patch_wall(wallid):
    wall = Wall.query.get_or_404(wallid)
    data = request.get_json() or {}
    wall.patch_from_dict(data)
    db.session.commit()
    return jsonify(wall.to_dict())

@bp.route('/walls/<int:wallid>', methods=['DELETE'])
def delete_wall(wallid):
    wall = Wall.query.get_or_404(wallid)
    db.session.delete(wall)
    db.session.commit()
    return jsonify(wall.to_dict())

@bp.route('/walls', methods=['DELETE'])
def delete_walls():
    auth = request.args.get('auth', 'notme', type=str)
    if auth != 'me':
        return unauthorized('wrong auth')
    number_items = db.session.query(Wall).delete()
    db.session.commit()
    return jsonify(number_items)

@bp.route('/walls/imgs', methods=['GET'])
def list_walls_img():
    mypath = join(app.config['STATIC_FOLDER'], 'walls')
    walls = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return jsonify(walls)
