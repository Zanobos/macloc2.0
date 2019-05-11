from app import db, socketio
from app.api import bp
from app.models import Climb, User, Wall
from app.worker import PublisherThread
from app.api.errors import bad_request, unauthorized
from flask import request, jsonify, url_for
from flask import current_app as app

#Ok for dev environment and in order to save on resources
publisher_thread_map = {}

@bp.route('/climbs/<int:climbid>', methods=['GET'])
def get_climb(climbid):
    return jsonify(Climb.query.get_or_404(climbid).to_dict())

@bp.route('/climbs', methods=['GET'])
def get_climbs():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 1000, type=int), 1000)
    user_id = request.args.get('user_id', None, type=int)
    status = request.args.get('status', None, type=str)
    not_status = request.args.get('not_status', None, type=str)
    if status is not None and not_status is not None:
        return bad_request('only one between status and not_status')
    query = Climb.query if user_id is None else Climb.query.filter(Climb.user_id == user_id)
    if status is not None:
        query = query.filter(Climb.status == status)
    elif not_status is not None:
        query = query.filter(Climb.status != not_status)
    else:
        query.filter(Climb.status == 'end')
    data = Climb.to_collection_dict(query, page, per_page, 'api.get_climbs')
    return jsonify(data)

@bp.route('/climbs', methods=['POST'])
def create_climb():
    #Create a new Climb, freezing wall and holds status
    #In any case, wallid and holdids are the ones from the ongoing wall
    user_id = request.args.get('user_id', None, type=int)
    wall_id = request.args.get('wall_id', None, type=int)
    if user_id is None or wall_id is None:
        return bad_request('must include user_id and wall_id as query param')
    user = User.query.get_or_404(user_id)
    wall = Wall.query.get_or_404(wall_id)
    historic_wall = wall.to_historic_wall()
    climb = Climb(climber=user, on_wall=historic_wall, going_on=wall, status='ready')
    db.session.add(climb)
    db.session.commit()
    response = jsonify(climb.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_climb', climbid=climb.id)
    return response

@bp.route('/climbs/<int:climbid>', methods=['PUT'])
def update_climb(climbid):
    climb = Climb.query.get_or_404(climbid)
    data = request.get_json() or {}
    climb.from_dict(data)
    db.session.commit()
    return jsonify(climb.to_dict())

@bp.route('/climbs/<int:climbid>', methods=['PATCH'])
def patch_climb(climbid):
    climb = Climb.query.get_or_404(climbid)
    data = request.get_json() or {}
    climb.patch_from_dict(data)
    wall_id = climb.going_on.id
    db.session.commit() # To close the open session (lazy load)
    global publisher_thread_map
    if data['status'] == 'start':
        climb.start_climb()
        publisher_thread = PublisherThread(climb=climb, db_session=db.session)
        publisher_thread.start()
        publisher_thread_map[wall_id] = publisher_thread
    if data['status'] == 'end':
        publisher_thread = publisher_thread_map[wall_id]
        publisher_thread.join()
        del publisher_thread_map[wall_id]
        # this end climb must be the last instruction because it touches the session
        climb.end_climb()
    db.session.commit()
    return jsonify(climb.to_dict())

@bp.route('/climbs/<int:climbid>', methods=['DELETE'])
def delete_climb(climbid):
    climb = Climb.query.get_or_404(climbid)
    # jsonify before deleting or foreign keys do not work
    deleted_hold = jsonify(climb.to_dict())
    db.session.delete(climb)
    db.session.commit()
    return deleted_hold

@bp.route('/climbs', methods=['DELETE'])
def delete_climbs():
    auth = request.args.get('auth', 'notme', type=str)
    if auth != 'me':
        return unauthorized('wrong auth')
    number_items = db.session.query(Climb).delete()
    db.session.commit()
    return jsonify(number_items)

@socketio.on('connect', namespace='/api/climbs')
def climbs_ws_connect():
    app.logger.info('Client connected')

@socketio.on('disconnect', namespace='/api/climbs')
def climbs_ws_disconnect():
    app.logger.info('Client disconnected')

# In case of exceptional failure resume publisher threads at startup
@bp.before_app_first_request
def resume_publisher_threads():
    climbs = Climb.query.filter(Climb.status == 'start').all()
    if not climbs:
        app.logger.info('no climbs in start status')
        return
    # First get all the possible wallids
    for climb in climbs:
        climb.tmp_wall_id = climb.going_on.id
        app.logger.info('climb {} on wall {} in start status'.format(climb.id, climb.tmp_wall_id))
        db.session.commit() # To close the open session (lazy load)
    global publisher_thread_map
    for climb in climbs:
        publisher_thread = PublisherThread(climb=climb, db_session=db.session)
        publisher_thread.start()
        publisher_thread_map[climb.tmp_wall_id] = publisher_thread
