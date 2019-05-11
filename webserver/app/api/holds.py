from app import db, socketio
from app.api import bp
from app.models import Hold
from app.api.errors import bad_request, unauthorized
from app.worker import CalibrationThread
from flask import request, jsonify, url_for
from flask import current_app as app

@bp.route('/holds/<int:holdid>', methods=['GET'])
def get_hold(holdid):
    return jsonify(Hold.query.get_or_404(holdid).to_dict())

@bp.route('/holds', methods=['GET'])
def get_holds():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 1000, type=int), 1000)
    wall_id = request.args.get('wall_id', None, type=int)
    query = Hold.query if wall_id is None else Hold.query.filter(Hold.wall_id == wall_id)
    data = Hold.to_collection_dict(query, page, per_page, 'api.get_holds')
    return jsonify(data)

@bp.route('/holds', methods=['POST'])
def create_hold():
    data = request.get_json() or {}
    if 'dist_from_sx' not in data or 'dist_from_bot' not in data or 'hold_type' not in data:
        return bad_request('must include dist_from_sx and dist_from_bot and hold_type')
    hold = Hold()
    hold.from_dict(data)
    db.session.add(hold)
    db.session.commit()
    response = jsonify(hold.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_hold', holdid=hold.id)
    return response

@bp.route('/holds/<int:holdid>', methods=['PUT'])
def update_hold(holdid):
    hold = Hold.query.get_or_404(holdid)
    data = request.get_json() or {}
    hold.from_dict(data)
    db.session.commit()
    return jsonify(hold.to_dict())

@bp.route('/holds/<int:holdid>', methods=['PATCH'])
def patch_hold(holdid):
    hold = Hold.query.get_or_404(holdid)
    data = request.get_json() or {}
    hold.patch_from_dict(data)
    db.session.commit()
    return jsonify(hold.to_dict())

@bp.route('/holds/<int:holdid>', methods=['DELETE'])
def delete_hold(holdid):
    hold = Hold.query.get_or_404(holdid)
    db.session.delete(hold)
    db.session.commit()
    return jsonify(hold.to_dict())

@bp.route('/holds', methods=['DELETE'])
def delete_holds():
    auth = request.args.get('auth', 'notme', type=str)
    if auth != 'me':
        return unauthorized('wrong auth')
    number_items = db.session.query(Hold).delete()
    db.session.commit()
    return jsonify(number_items)

@socketio.on('connect', namespace='/api/holds')
def holds_ws_connect():
    app.logger.info('Calibration client connected')

@socketio.on('disconnect', namespace='/api/holds')
def holds_ws_disconnect():
    app.logger.info('Calibration client disconnected')

@socketio.on('message', namespace='/api/holds')
def holds_ws_message(message):
    app.logger.info('message ', message)
    calibration_thread = CalibrationThread(db_session=db.session, hold_info=message)
    calibration_thread.start()
    calibration_thread.join()
