import os
from sqlalchemy import (Column, String, Integer, DateTime, Time,
                        ForeignKey, create_engine)
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "class_scheduler"
    database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Class
Have class details
'''


class Class(db.Model):
    __tablename__ = 'class'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    code = Column(String(80))
    end_date = Column(DateTime(timezone=True), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    created_date = Column(DateTime(timezone=True), nullable=False)
    modified_date = Column(DateTime(timezone=True), nullable=False)
    instructor_id = Column(
        Integer,
        ForeignKey('instructor.id'),
        nullable=False)
    lecture = db.relationship(
        'Lecture',
        backref='class',
        cascade='all, delete-orphan',
        lazy=True)

    def __init__(
            self,
            name,
            code,
            end_date,
            start_date,
            created_date,
            modified_date,
            instructor_id):
        self.name = name
        self.code = code
        self.end_date = end_date
        self.start_date = start_date
        self.created_date = created_date
        self.modified_date = modified_date
        self.instructor_id = instructor_id
        # self.lecture = lecture

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'end_date': self.end_date,
            'start_date': self.start_date,
            'created_date': self.created_date,
            'modified_date': self.modified_date,
            'instructor_id': self.instructor_id
        }


'''
Classroom
Classroom location and name
'''


class Classroom(db.Model):
    __tablename__ = 'classroom'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    building = Column(String(120))
    floor = Column(String(1))
    occupancy = Column(Integer)
    created_date = Column(DateTime(timezone=True), nullable=False)
    modified_date = Column(DateTime(timezone=True), nullable=False)
    lecture = db.relationship(
        'Lecture',
        backref='classroom',
        cascade='all, delete-orphan',
        lazy=True)
    hours = db.relationship(
        'Hours',
        backref='classroom',
        cascade='all, delete-orphan',
        lazy=True)

    def __init__(
            self,
            name,
            building,
            floor,
            occupancy,
            created_date,
            modified_date):
        self.name = name
        self.building = building
        self.floor = floor
        self.occupancy = occupancy
        self.created_date = created_date
        self.modified_date = modified_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'building': self.building,
            'floor': self.floor,
            'occupancy': self.occupancy,
            'created_date': self.created_date,
            'modified_date': self.modified_date
        }


'''
Instructor
Instructor details
'''


class Instructor(db.Model):
    __tablename__ = 'instructor'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    created_date = Column(DateTime(timezone=True), nullable=False)
    modified_date = Column(DateTime(timezone=True), nullable=False)
    classes = db.relationship(
        'Class',
        backref='instructor',
        cascade='all, delete-orphan',
        lazy=True)

    def __init__(self, name, created_date, modified_date):
        self.name = name
        self.created_date = created_date
        self.modified_date = modified_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_date': self.created_date,
            'modified_date': self.modified_date
        }


'''
Lecture
Lecture details with class_id and classroom_id.
'''


class Lecture(db.Model):
    __tablename__ = 'lecture'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    class_id = Column(Integer, ForeignKey('class.id'), nullable=False)
    classroom_id = Column(Integer, ForeignKey('classroom.id'), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    created_date = Column(DateTime(timezone=True), nullable=False)
    modified_date = Column(DateTime(timezone=True), nullable=False)

    def __init__(
            self,
            name,
            class_id,
            classroom_id,
            start_time,
            end_time,
            created_date,
            modified_date):
        self.name = name
        self.class_id = class_id
        self.classroom_id = classroom_id
        self.start_time = start_time
        self.end_time = end_time
        self.created_date = created_date
        self.modified_date = modified_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'class_id': self.class_id,
            'classroom_id': self.classroom_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'created_date': self.created_date,
            'modified_date': self.modified_date
        }


'''
Hours
Classroom hours with foreign key to classroom_id
'''


class Hours(db.Model):
    __tablename__ = 'hours'

    id = Column(Integer, primary_key=True)
    day = Column(Integer, nullable=False)
    open_time = Column(Time(timezone=True))
    close_time = Column(Time(timezone=True))
    classroom_id = Column(Integer, ForeignKey('classroom.id'), nullable=False)

    def __init__(self, day, open_time, close_time, classroom_id):
        self.day = day
        self.open_time = open_time
        self.close_time = close_time
        self.classroom_id = classroom_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'day': self.day,
            'open_time': str(self.open_time),
            'close_time': str(self.close_time),
            'classroom_id': self.classroom_id
        }
