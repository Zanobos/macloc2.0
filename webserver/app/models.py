from datetime import datetime
from app import db
from flask import url_for

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs)
                        if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs)
                        if resources.has_prev else None
            }
        }
        return data

class User(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    nickname = db.Column(db.String(20), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    climbs = db.relationship('Climb', backref='climber', lazy='dynamic')

    def __repr__(self):
        return '<User {} ({})>'.format(self.name, self.nickname)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'nickname': self.nickname,
            'email': self.email,
            'height': self.height,
            'weight': self.weight
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'height', 'weight','nickname','email']:
            setattr(self, field, data[field])
        return self

    def patch_from_dict(self, data):
        for field in data:
            setattr(self, field, data[field])
        return self

# Remember, user can be referenced with relationship, but
# holds and walls must be copied because they can change
# For this reason I store wall information as attributes
class Climb(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    historic_wall_id = db.Column(db.Integer, db.ForeignKey('historic_wall.id'))
    wall_id = db.Column(db.Integer, db.ForeignKey('wall.id'))
    status = db.Column(db.String(20))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)

    def __repr__(self):
        return '<Climb {}>'.format(self.id)

    def to_dict(self):
        return self.to_dict_complete(False)

    def to_dict_complete(self, historic):
        wall_id = self.historic_wall_id if historic is True else self.wall_id
        data = {
            'id': self.id,
            'climber_name': self.climber.name,
            'wall_grade': self.on_wall.grade,
            'wall_id': wall_id,
            'status': self.status,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration
        }
        return data

    def from_dict(self, data):
        for field in []:
            setattr(self, field, data[field])
        return self

    def patch_from_dict(self, data):
        for field in data:
            setattr(self, field, data[field])
        return self

    def start_climb(self):
        self.status = 'start'
        self.start_time = datetime.now()
        self.going_on.active = True

    def end_climb(self):
        self.status = 'end'
        self.end_time = datetime.now()
        self.going_on.active = False
        self.duration = (self.end_time - self.start_time).seconds

class Wall(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float)
    width = db.Column(db.Float)
    grade = db.Column(db.Float)
    active = db.Column(db.Boolean)
    img = db.Column(db.String(120))
    holds = db.relationship('Hold', backref='mounted_on', lazy='dynamic')
    climb = db.relationship('Climb', uselist=False, backref='going_on')

    def __repr__(self):
        return '<Wall {}, h={}, w={}, active={}>' .format(self.id, self.height, self.width,
                                                          self.active)

    def to_dict(self):
        data = {
            'id': self.id,
            'height': self.height,
            'width': self.width,
            'grade': self.grade,
            'img': self.img,
            'active': self.active,
            'holds_number': len(self.holds.all())
        }
        return data

    def from_dict(self, data):
        for field in ['height', 'width', 'grade', 'active']:
            setattr(self, field, data[field])
        return self

    def patch_from_dict(self, data):
        for field in data:
            setattr(self, field, data[field])
        return self

    def to_historic_wall(self):
        hw = HistoricWall().from_dict(self.to_dict())
        hw.holds = [h.to_historic_hold() for h in self.holds]
        return hw

class Hold(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    can_id = db.Column(db.Integer)
    dist_from_sx = db.Column(db.Float)
    dist_from_bot = db.Column(db.Float)
    hold_type = db.Column(db.String(30))
    wall_id = db.Column(db.Integer, db.ForeignKey('wall.id'))

    def __repr__(self):
        return '<Hold {}, can_id={} ({},{}) t={}>'.format(self.id, self.can_id, self.dist_from_sx, \
                self.dist_from_bot, self.hold_type)

    def to_dict(self):
        data = {
            'id': self.id,
            'can_id': self.can_id,
            'dist_from_sx': self.dist_from_sx,
            'dist_from_bot': self.dist_from_bot,
            'hold_type': self.hold_type,
            'wall_id': self.wall_id
        }
        return data

    def from_dict(self, data):
        for field in ['can_id', 'dist_from_sx', 'dist_from_bot', 'hold_type', 'wall_id']:
            setattr(self, field, data[field])
        return self

    def patch_from_dict(self, data):
        for field in data:
            setattr(self, field, data[field])
        return self

    def to_historic_hold(self):
        return HistoricHold().from_dict(self.to_dict())

class HistoricWall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float)
    width = db.Column(db.Float)
    grade = db.Column(db.Float)
    img = db.Column(db.String(120))
    holds = db.relationship('HistoricHold', backref='mounted_on', lazy='dynamic')
    climb = db.relationship('Climb', uselist=False, backref='on_wall')

    def __repr__(self):
        return '<HistoricWall {}, h={}, w={}>' .format(self.id, self.height, self.width)

    def to_dict(self):
        data = {
            'id': self.id,
            'height': self.height,
            'width': self.width,
            'grade': self.grade,
            'img': self.img
        }
        return data

    def from_dict(self, data):
        for field in ['height', 'width', 'grade','img']:
            setattr(self, field, data[field])
        return self

class HistoricHold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    can_id = db.Column(db.Integer)
    dist_from_sx = db.Column(db.Float)
    dist_from_bot = db.Column(db.Float)
    hold_type = db.Column(db.String(30))
    wall_id = db.Column(db.Integer, db.ForeignKey('historic_wall.id'))
    records = db.relationship('Record', backref='of_hold', lazy='dynamic')

    def __repr__(self):
        return '<HistoricHold {}, can_id={} ({},{}) t={}>'.format(self.id, self.can_id, \
                self.dist_from_sx, self.dist_from_bot, self.hold_type)

    def to_dict(self):
        data = {
            'id': self.id,
            'can_id': self.can_id,
            'dist_from_sx': self.dist_from_sx,
            'dist_from_bot': self.dist_from_bot,
            'hold_type': self.hold_type
        }
        return data

    def from_dict(self, data):
        for field in ['can_id', 'dist_from_sx', 'dist_from_bot', 'hold_type']:
            setattr(self, field, data[field])
        return self

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    can_id = db.Column(db.Integer)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    z = db.Column(db.Float)
    timestamp = db.Column(db.Integer)
    hold_id = db.Column(db.Integer, db.ForeignKey('historic_hold.id'))
    climb_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Record {}, can_id={}, x={}, y={}, z={}>'.format(self.id, self.can_id,
                                                                 self.x, self.y, self.z)

    def to_dict(self):
        data = {
            'id': self.id,
            'can_id': self.can_id,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'hold_id': self.hold_id,
            'timestamp': self.timestamp
        }
        return data

    def to_ws_dict(self):
        data = {
            'hold_id': self.hold_id,
            'x': self.x,
            'y': self.y,
            'z': self.z
        }
        return data
