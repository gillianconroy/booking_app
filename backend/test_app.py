import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Instructor, Classroom, Class, Lecture, Hours
from auth import AuthError, requires_auth

class SchedulerTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "class_scheduler_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.faculty = { 'Authorization': 'Bearer {}'.format(os.environ['auth_token_faculty'])}
        self.instructor = { 'Authorization': 'Bearer {}'.format(os.environ['auth_token_instructor'])}
        self.faculty_expired = { 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBzZmhtOVNweWZjbDE0czNBbDlERCJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjcy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViMTc1Mzg2YjY5YmMwYzEyZjczYjZjIiwiYXVkIjoiYm9va2luZyIsImlhdCI6MTU5NDE3Nzc2MywiZXhwIjoxNTk0MTg0OTYzLCJhenAiOiJOVEJyaVFiRzhJc0Rja0xTaFJDZ3ZzNkRIcXNFN0QyMiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNsYXNzIiwiZGVsZXRlOmNsYXNzcm9vbSIsImRlbGV0ZTppbnN0cnVjdG9yIiwiZGVsZXRlOmxlY3R1cmUiLCJnZXQ6Y2xhc3MiLCJnZXQ6Y2xhc3Nyb29tIiwiZ2V0Omluc3RydWN0b3IiLCJnZXQ6bGVjdHVyZSIsInBhdGNoOmNsYXNzIiwicGF0Y2g6Y2xhc3Nyb29tIiwicGF0Y2g6aW5zdHJ1Y3RvciIsInBhdGNoOmxlY3R1cmUiLCJwb3N0OmNsYXNzIiwicG9zdDpjbGFzc3Jvb20iLCJwb3N0Omluc3RydWN0b3IiLCJwb3N0OmxlY3R1cmUiXX0.B7iNMJunzmDLTAJuRHVRCrUpwun0gE8OuwPaBfUIAXX90qqtDniQxrfl7PSEkZmSaJVHSTEIZEsrPjqd2J7CThHcbhAz2vy4t-GtsaMWbPpmjWNWABVWrjroVMhFzu6mUNwngyTA7peGfSkRQhGL0dt6cBhAOxomwBLRh12uCRUFzmRZHx7Z4oH2etIEsku213KiQQnJmQ1mlKebnDB9D2m0BmBCC6uA9ViK18DII7uw2JTQ2OBowXo2F6tf67ftiTVMZatcRcnuHdrSiTOyRUVEWkD101HDUbDbL5r_HdL96Ya4i2rn4--V6Zu4sIxcbjDx00_jNYrnXBUKzAwiXQ'.format() }

        self.new_lecture = {
            "name": "Attention and Distraction",
            "class_id": 10,
            "classroom_id": 5,
            "start_time": "2020-03-01 8:00:25-04",
            "end_time": "2020-03-01 8:59:25-04"
        }

        self.invalid_date = {
            "name": "Attention and Distraction",
            "class_id": 10,
            "classroom_id": 5,
            "start_time": "2020-05-01 8:00:25-04",
            "end_time": "2020-05-01 8:59:25-04"
        }

        self.invalid_hours = {
            "name": "Attention and Distraction",
            "class_id": 10,
            "classroom_id": 5,
            "start_time": "2020-03-01 6:00:25-04",
            "end_time": "2020-03-01 7:59:25-04"
        }

        self.invalid_classroom_id = {
            "name": "Attention and Distraction",
            "class_id": 10,
            "classroom_id": 8,
            "start_time": "2020-03-01 8:00:25-04",
            "end_time": "2020-03-01 8:59:25-04"
        }
        
        self.invalid_class_id = {
            "name": "Attention and Distraction",
            "class_id": 20,
            "classroom_id": 5,
            "start_time": "2020-03-01 8:00:25-04",
            "end_time": "2020-03-01 8:59:25-04"
        }

        self.end_time_before_start_time = {
            "name": "Attention and Distraction",
            "class_id": 10,
            "classroom_id": 5,
            "start_time": "2020-03-01 9:00:25-04",
            "end_time": "2020-03-01 8:00:25-04"
        }

        self.start_end_different_days = {
            "name": "Attention and Distraction",
            "class_id": 10,
            "classroom_id": 5,
            "start_time": "2020-03-01 9:00:25-04",
            "end_time": "2020-03-02 8:00:25-04"
        }

        self.update_lecture = {
            "name": "Ongoing Home Care",
            "class_id": 7,
            "classroom_id": 5,
            "start_time": "2020-03-01 8:00:25-04",
            "end_time": "2020-03-01 8:59:25-04"
        }

        self.update_with_no_dates = {
            "name": "Ongoing Home Care",
            "class_id": 7,
            "classroom_id": 5
        }

        self.missing_data = {
            "class_id": None,
            "classroom_id": 5,
            "start_time": "2020-11-22 11:10:25-04",
            "end_time": ""
        }
        
        self.search = {
            "date": "2020-06-10",
            "occupancy": 80
        }

        self.search_missing_data = {
            "date": "2020-06-10"
        }


    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_lectures(self):
        """Test get all lectures"""
        res = self.client().get('/lecture', headers=self.faculty)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['lecture'])
        self.assertTrue(data['num_lectures'])

    def test_405_fail_post_method_on_get_lectures(self):
        """Test 405 wrong method to retrieve lectures endpoint"""
        res = self.client().post('/lecture', headers=self.faculty)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'method not allowed')

    def test_403_fail_get_all_lectures_no_permission(self):
        """Test 403 error get all lectures with invalid permissions"""
        res = self.client().get('/lecture', headers=self.instructor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_401_fail_lectures_error_no_JWT(self):
        """Test 401 error code if no JWT present"""
        res = self.client().get('/lecture')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_401_fail_lectures_error_expired_JWT(self):
        """Test 401 error code if JWT expired"""
        res = self.client().get('/lecture', headers=self.faculty_expired)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Token expired.')

    def test_get_lecture_by_id(self):
        """Test get lecture by instructor id"""
        res = self.client().get('/instructor/1/lecture', headers=self.instructor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['lecture'])
        self.assertTrue(data['num_lectures'])

    def test_404_fail_get_lecture_id_out_of_index(self):
        """Test 404 error get lecture where instructor id is out of index"""
        res = self.client().get('/instructor/8/lecture', headers=self.instructor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_new_lecture(self):
        """Test post new lecture"""
        res = self.client().post('/lecture/add', headers=self.instructor, json=self.new_lecture)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['new_lecture'])
        self.assertTrue(data['num_lectures'])

    def test_422_fail_post_new_lecture_date_span(self):
        """Test 422 error post new lecture with date spans over one day"""
        res = self.client().post('/lecture/add', headers=self.instructor, json=self.start_end_different_days)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_fail_post_new_lecture_invalid_hours(self):
        """Test 422 error post new lecture with end_time before start_time"""
        res = self.client().post('/lecture/add', headers=self.instructor, json=self.end_time_before_start_time)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_404_fail_post_new_lecture_class_id_invalid(self):
        """Test 404 error post new lecture with invalid class_id"""
        res = self.client().post('/lecture/add', headers=self.instructor, json=self.invalid_class_id)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_fail_post_new_lecture_classroom_id_invalid(self):
        """Test 404 error post new lecture with invalid classroom_id"""
        res = self.client().post('/lecture/add', headers=self.instructor, json=self.invalid_classroom_id)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_fail_post_new_lecture_beyond_dates(self):
        """Test 422 error post new lecture with date outside of class semester dates"""
        res = self.client().post('/lecture/add', headers=self.instructor, json=self.invalid_date)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_fail_post_new_lecture_beyond_classroom_hours(self):
        """Test 422 error post new lecture with hours outside of classroom hours"""
        res = self.client().post('/lecture/add', headers=self.instructor, json=self.invalid_hours)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_fail_post_lecture_missing_data(self):
        """Test 422 error existing lecture with missing parameters"""
        res = self.client().post('/lecture/add', headers=self.instructor, json=self.missing_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_patch_lecture(self):
        """Test patch existing lecture"""
        res = self.client().patch('/lecture/8', headers=self.instructor, json=self.update_lecture)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['lecture'])

# @TODO test for INSTRUCTOR permissions - get resource that belongs to them

    def test_404_fail_patch_lecture_invalid_id(self):
        """Test 404 error lecture id beyond index"""
        res = self.client().patch('/lecture/300', headers=self.instructor, json=self.update_lecture)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_fail_patch_lecture_missing_data(self):
        """Test 422 error existing lecture with missing data"""
        res = self.client().patch('/lecture/8', headers=self.instructor, json=self.missing_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')


# @TODO test for INSTRUCTOR permissions - get resource that belongs to them

    # def test_delete_lecture(self):
    #     """Test delete existing lecture"""
    #     res = self.client().delete('/lecture/5', headers=self.instructor)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['deleted_lecture'], 5)
    #     self.assertTrue(data['num_lectures'])

    def test_404_fail_delete_lecture_id_beyond_index(self):
        """Test 404 error delete lecture where id does not exist"""
        res = self.client().delete('/lecture/500', headers=self.instructor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_search(self):
        """Test search for available classrooms"""
        res = self.client().post('/search', headers=self.instructor, json=self.search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['classrooms'])
        self.assertTrue(data['bookings'])

    def test_422_fail_search_missing_parameters(self):
        """Test 422 error code on missing parameters"""
        res = self.client().post('/search', headers=self.instructor, json=self.search_missing_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
