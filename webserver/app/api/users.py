from app import db
from app.api import bp
from app.models import User
from app.api.errors import bad_request, unauthorized
from flask import request, jsonify, url_for

@bp.route('/users/<int:userid>', methods=['GET'])
def get_user(userid):
    return jsonify(User.query.get_or_404(userid).to_dict())

@bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 1000, type=int), 1000)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'name' not in data or 'height' not in data or 'weight' not in data:
        return bad_request('must include name, height and weight')
    user = User()
    user.from_dict(data)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', userid=user.id)
    return response

@bp.route('/users/<int:userid>', methods=['PUT'])
def update_user(userid):
    user = User.query.get_or_404(userid)
    data = request.get_json() or {}
    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/users/<int:userid>', methods=['PATCH'])
def patch_user(userid):
    user = User.query.get_or_404(userid)
    data = request.get_json() or {}
    user.patch_from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/users/<int:userid>', methods=['DELETE'])
def delete_user(userid):
    user = User.query.get_or_404(userid)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/users', methods=['DELETE'])
def delete_users():
    auth = request.args.get('auth', 'notme', type=str)
    if auth != 'me':
        return unauthorized('wrong auth')
    number_items = db.session.query(User).delete()
    db.session.commit()
    return jsonify(number_items)
