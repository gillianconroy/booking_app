import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, func
from flask_cors import CORS
from models import setup_db

from datetime import datetime, timezone, time
import calendar

# try different things to avoid logging errors
# import logging
# import logging.config
# from logging import Formatter, FileHandler

# logging.config.fileConfig('logging.conf')

# # create logger
# logger = logging.getLogger('simpleExample')

# # 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')

import json

from models import *
from auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    Homepage
    '''
    @app.route('/', methods=['GET'])
    def get_home():
        return jsonify({
            "success": True,
            "message": "WELCOME TO MY HEROKU API!! \
                Please specify which resource you would like to request! 🤓"
        })

    '''
    GET:Lecture
    Returns all lectures from DB
    '''
    @app.route('/lecture', methods=['GET'])
    @requires_auth('get:alllecture')
    def get_lecture(jwt):
        try:
            alllectures = Lecture.query.all()
            lectures = [l.format() for l in alllectures]
        except BaseException:
            abort(404)
        return jsonify({
            "success": True,
            "lecture": lectures,
            "num_lectures": len(lectures)
        })

    '''
    GET:Lecture by instructor_id
    Returns all lectures from DB with instructor_id
    '''
    @app.route('/instructor/<instructor_id>/lecture', methods=['GET'])
    @requires_auth('get:lecture')
    def get_lecture_by_id(jwt, instructor_id):
        if Instructor.query.get(instructor_id) is None:
            abort(404)
        try:
            lecture_by_id = Lecture.query.join('class').filter(
                Class.instructor_id == instructor_id).all()
            lectures = [l.format() for l in lecture_by_id]
        except BaseException:
            abort(404)
        return jsonify({
            "success": True,
            "lecture": lectures,
            "num_lectures": len(lectures)
        })

    '''
    POST:Lecture
    Posts a new lecture/booking to the database
    '''
    @app.route('/lecture/add', methods=['POST'])
    @requires_auth('post:lecture')
    def post_lecture(jwt):
        response = request.get_json()
        now = datetime.now(tz=None)

        name = response.get('name')
        class_id = response.get('class_id')
        classroom_id = response.get('classroom_id')
        start_time = response.get('start_time')
        end_time = response.get('end_time')
        created_date = now
        modified_date = now

        if all([name, class_id, classroom_id, start_time, end_time]):
            # split date string into date string
            start_date = start_time.split(' ')[0]
            end_date = end_time.split(' ')[0]

            # split date string into time string
            start_time_str = start_time.split(' ')[1]
            end_time_str = end_time.split(' ')[1]

            # Check that bookings start and end on the same date.
            if end_date != start_date:
                print("booking must start and end on the same day")
                abort(422)

            # Create datetime object for comparison. Remove timezone.
            start_time_obj = datetime.strptime(
                start_time[:-3], '%Y-%m-%d %H:%M:%S')
            end_time_obj = datetime.strptime(
                end_time[:-3], '%Y-%m-%d %H:%M:%S')

            int_of_dow = start_time_obj.weekday()

            # Check if start_time is before end_time:
            if end_time_obj <= start_time_obj:
                print("end time must be after start time")
                abort(422)

            # Check if class_id is valid:
            if Class.query.get(class_id) is None:
                print(f'class {class_id} does not exist')
                abort(404)

            # Check if classroom_id is valid:
            if Classroom.query.get(classroom_id) is None:
                print(f'classroom {classroom_id} does not exist')
                abort(404)

            # Check that lecture is within class start and end dates
            if Class.query.filter(Class.id == class_id).filter(func.date(
               Class.start_date) <= start_date, func.date(Class.end_date)
                    >= end_date).one_or_none() is None:
                print(f'{start_date} is not within class semester dates')
                abort(422)

            # Check that lecture is within specified classroom hours
            if Hours.query.filter(Hours.classroom_id == classroom_id).filter(
               Hours.day == int_of_dow, Hours.open_time <= start_time_str,
               Hours.close_time >= end_time_str).one_or_none() is None:
                print(f'times are not within classroom {classroom_id} hours')
                abort(422)

        else:
            print('missing parameters')
            abort(422)

        try:
            new_lecture = Lecture(
                name=name,
                class_id=class_id,
                classroom_id=classroom_id,
                start_time=start_time,
                end_time=end_time,
                created_date=json.dumps(
                    created_date,
                    default=str),
                modified_date=json.dumps(
                    modified_date,
                    default=str))
            new_lecture.insert()
        except Exception as e:
            print(e)
            abort(422)
        return jsonify({
            "success": True,
            "new_lecture": [new_lecture.format()],
            "num_lectures": Lecture.query.count()
        })

    '''
    PATCH:Lecture
    Updates an existing lecture by id. If id returns none, abort.
    '''
    @app.route('/lecture/<lecture_id>', methods=['PATCH'])
    @requires_auth('patch:lecture')
    def patch_lecture(jwt, lecture_id):
        # if jwt role is Instructor:
        # check that resource belongs to them

        if Lecture.query.get(lecture_id) is None:
            print(f'lecture {lecture_id} does not exist')
            abort(404)

        response = request.get_json()
        now = datetime.now(tz=None)

        name = response.get('name')
        class_id = response.get('class_id')
        classroom_id = response.get('classroom_id')
        start_time = response.get('start_time')
        end_time = response.get('end_time')
        modified_date = now

        if all([name, class_id, classroom_id, start_time, end_time]):
            # split date string into date string
            start_date = start_time.split(' ')[0]
            end_date = end_time.split(' ')[0]

            # split date string into time string
            start_time_str = start_time.split(' ')[1]
            end_time_str = end_time.split(' ')[1]

            # Check that bookings start and end on the same date.
            if end_date != start_date:
                print("booking must start and end on the same day")
                abort(422)

            # Create datetime object for comparison. Remove timezone.
            start_time_obj = datetime.strptime(
                start_time[:-3], '%Y-%m-%d %H:%M:%S')
            end_time_obj = datetime.strptime(
                end_time[:-3], '%Y-%m-%d %H:%M:%S')

            int_of_dow = start_time_obj.weekday()

            # Check if start_time is before end_time:
            if end_time_obj <= start_time_obj:
                print("end time must be after start time")
                abort(422)

            # Check if classroom_id is valid:
            if Classroom.query.get(classroom_id) is None:
                print(f'classroom {classroom_id} does not exist')
                abort(404)

            # Check if class_id is valid:
            if Class.query.get(class_id) is None:
                print(f'class {class_id} does not exist')
                abort(404)

            # Check that lecture is within class start and end dates
            if Class.query.filter(Class.id == class_id).filter(func.date(
               Class.start_date) <= start_date, func.date(Class.end_date)
                    >= end_date).one_or_none() is None:
                print(f'{start_date} is not within class semester dates')
                abort(422)

            # Check that lecture is within specified classroom hours
            if Hours.query.filter(Hours.classroom_id == classroom_id).filter(
               Hours.day == int_of_dow, Hours.open_time <= start_time_str,
               Hours.close_time >= end_time_str).one_or_none() is None:
                print(f'times are not within classroom {classroom_id} hours')
                abort(422)

        else:
            print('missing parameters')
            abort(422)

        try:
            get_lecture = Lecture.query.filter(
                Lecture.id == lecture_id).one_or_none()
            get_lecture.name = name
            get_lecture.class_id = class_id
            get_lecture.classroom_id = classroom_id
            get_lecture.modified_date = json.dumps(modified_date, default=str)
            get_lecture.start_time = json.dumps(start_time)
            get_lecture.end_time = json.dumps(end_time)
            get_lecture.update()
        except Exception as e:
            print(e)
            abort(422)
        return jsonify({
            "success": True,
            "lecture": [get_lecture.format()]
        })

    '''
    DELETE:Lecture
    Deletes an existing lecture in the database by id.
    If id returns none, abort.
    '''
    @app.route('/lecture/<lecture_id>', methods=['DELETE'])
    @requires_auth('delete:lecture')
    def delete_lecture(jwt, lecture_id):
        del_lecture = Lecture.query.filter(
            Lecture.id == lecture_id).one_or_none()
        if del_lecture is None:
            abort(404)
        try:
            del_lecture.delete()
        except Exception as e:
            print(e)
            abort(422)
        return jsonify({
            "success": True,
            "deleted_lecture": del_lecture.id,
            "num_lectures": Lecture.query.count()
        })

    '''
    POST: Search
    Get classroom booking slot by date availability and occupancy
    maximum, querying hours by classroom id.
    If lectures returns none, return classrooms.
    '''

    @app.route('/search', methods=['POST'])
    @requires_auth('get:classroom')
    def search(jwt):
        response = request.get_json()

        date = response.get('date')
        occupancy = response.get('occupancy')

        if all([date, occupancy]):
            date_time_obj = datetime.strptime(date, '%Y-%m-%d')
            int_of_dow = date_time_obj.weekday()

            results = Classroom.query.join('hours').filter(
                      Hours.day == int_of_dow,
                      Classroom.occupancy >= occupancy).all()

            classroom_ids = []
            for r in results:
                classroom_ids.append(r.id)
        else:
            print('missing parameters')
            abort(422)

        try:
            lec = Lecture.query.filter(Lecture.classroom_id.in_(
                classroom_ids)).filter(func.date(Lecture.start_time)
                                       >= date_time_obj).all()

        except Exception as e:
            print(e)
            abort(422)

        return jsonify({
            'success': True,
            'classrooms': [r.format() for r in results],
            'bookings': [l.format() for l in lec]
        })

    # Error Handling
    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error['description']
        }), AuthError.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
