# Full Stack Booking App Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Environment Setup

To setup environment variables using the `setup.sh` file, within your virtual environment run:

```bash
source setup.sh
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the  postgres database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.


## Database Setup

From your virtual environment, you will need to setup a database, with the following commands, and import the database from `class_scheduler.psql`.

```bash
dropdb class_scheduler 
createdb class_scheduler
psql class_scheduler < class_scheduler.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Tasks

### Setup Auth0

To set up Auth0 from scratch, follow the below instructions:

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:alllecture`
    - `get:classrooms`
    - `get:lecture`
    - `post:lecture`
    - `patch:lecture`
    - `delete:lecture`

6. Create new roles for:
    - Instructor
        - can `get:classrooms`, `get:lecture`, `post:lecture`, `patch:lecture`, `delete:lecture`
    - Faculty
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Instructor role to one and Faculty role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/Capstone.postman_collection.json`
    - Navigate to the authorization tab, and include the appropriate JWT you previously took down in the token field for the endpoint.
    - Run the collection and correct any errors.


INTRODUCTION
This Class Scheduler API is an interactive booking app that is created for Instructors and Faculty to better utilize classroom time slots by booking lectures in classrooms. This capstone project is part of the Full Stack Nanodegree Program designed by Udacity. The API is organized around REST. The API has resource-oriented URLs, accepts JSON request bodies, returns JSON-encoded responses, and uses standard HTTP response codes and verbs. It interacts with the database, and performs basic CRUD operations to manipulate the data. It also utilizes JWT to check for authentication permissions to access the endpoints.

To use this API, the user can run this on their local server, and it has been tested and deployed to run on Heroku. This API can be scaled to fit your needs. A portion of the app has already been built for essential end points, which are not included in this project, however, this project clearly utilizes the endpoints necessary to perform the booking of lectures necessary for the project.

GETTING STARTED
Base URL: If you pull the repo and run it on your local machine, it can be run at http://127.0.0.1:5000/ or http://localhost:5000/. It is also hosted live on Heroku https://class-scheduler-booking-app.herokuapp.com/. The base URL will not return much, so you must specify one of the resources listed below in order to return useful data.

API Keys/Authentication: Authentication is set up using a third-party authentication service, Auth0. Users permissions and roles are set up using the Auth0 interface, and the user accesses the JWT by the Auth0 login page. The endpoints take JWT permissions set up in Auth0, and authenticate the various endpoints. We chose to implement authorization and authentication using JWT via Auth0 rather than API keys.


ERRORS
Errors:
This API uses conventional HTTP response codes to indicate the success or failure of your API request. They are returned as a JSON object with the status code and message outlining the specific error response type.

Sample JSON object error message:
{
    "error": 404, 
    "message": "resource not found", 
    "success": false
}

This API uses:
200 - OK. Your API request was successful. Everything worked as expected.
404 - Not Found. The requested resource doesn't exist, indicating an API request failure based on the information provided. 
405 - Method Not Allowed. The API request failed due to the method being incorrect for the specified endpoint.
422 - Unprocessable Request. An API request failure based on the request being unprocessable to the backend.
500 - Internal Server Error. A general error that something has gone wrong on the server.


ENDPOINT LIBRARY:
List of Endpoints:
GET '/lecture'
GET '/instructor/<instructor_id>/lecture'
POST '/search'
POST '/lecture/add'
PATCH '/lecture/<lecture_id>'
DELETE '/lecture/<lecture_id>'

To test these endpoints, use Postman and pass in the JWT Bearer Token under the Authentication tab.


GET '/lecture'
- Fetches all lectures
- Request: Arguments: JWT Bearer Token
- Required permission: 'get:lecture'
Sample request:
http://localhost:5000/lecture

- Returns: 
An array of objects, with a single key, lecture, formatted as key:value pairs.
A count of the total number of lectures, and a success message is returned, indicating everything worked as expected.
Sample response body:
{
    "lecture": [
        {
            "class_id": 1,
            "classroom_id": 1,
            "created_date": "Tue, 07 Jul 2020 14:58:25 GMT",
            "end_time": "Thu, 22 Oct 2020 14:11:25 GMT",
            "id": 3,
            "modified_date": "Tue, 07 Jul 2020 14:58:25 GMT",
            "name": "Street Art",
            "start_time": "Thu, 22 Oct 2020 13:11:25 GMT"
        },
        {
            "class_id": 3,
            "classroom_id": 5,
            "created_date": "Tue, 07 Jul 2020 20:44:33 GMT",
            "end_time": "Thu, 22 Oct 2020 14:11:25 GMT",
            "id": 5,
            "modified_date": "Tue, 07 Jul 2020 20:44:33 GMT",
            "name": "Family care",
            "start_time": "Thu, 22 Oct 2020 13:11:25 GMT"
        }
    ],
    "num_lectures": 12,
    "success": true
}

GET 'instructor/<instructor_id>/lecture'
- Fetches all lectures by instructor id.
- Request: Arguments: JWT Bearer Token
- Required permission: 'get:lecture'
Sample request:
http://localhost:5000/instructor/1/lecture

- Returns: 
An array of objects, with a single key, lecture, formatted as key:value pairs.
A count of the total number of lectures, and a success message is returned, indicating everything worked as expected.
Sample response body:
{
    "lecture": [
        {
            "class_id": 1,
            "classroom_id": 1,
            "created_date": "Tue, 07 Jul 2020 14:58:25 GMT",
            "end_time": "Thu, 22 Oct 2020 14:11:25 GMT",
            "id": 3,
            "modified_date": "Tue, 07 Jul 2020 14:58:25 GMT",
            "name": "Street Art",
            "start_time": "Thu, 22 Oct 2020 13:11:25 GMT"
        },
        {
            "class_id": 4,
            "classroom_id": 4,
            "created_date": "Tue, 07 Jul 2020 20:55:14 GMT",
            "end_time": "Thu, 30 Jan 2020 13:11:25 GMT",
            "id": 11,
            "modified_date": "Tue, 07 Jul 2020 20:55:14 GMT",
            "name": "Old Hollywood",
            "start_time": "Thu, 30 Jan 2020 12:11:25 GMT"
        }
    ],
    "num_lectures": 8,
    "success": true
}

POST '/search'
- Search for available classrooms to book a lecture on a date string and occupancy maximum as an integer. If successful, results will be returned with available classrooms and current bookings.
- Request: Arguments(required): Send a JSON object with key:value pairs of keys: date, and occupancy. 
- Authentication: JWT Bearer Token. Required permission: 'get:classroom'
Sample request body:
{
"date": "2020-06-10",
"occupancy": 80
}
- Returns: An array of object with keys: classrooms and bookings will be returned, along with a simple 'success: True' message to indicate your request was processed as expected.
{
    "bookings": [
        {
            "class_id": 1,
            "classroom_id": 1,
            "created_date": "Tue, 07 Jul 2020 14:58:25 GMT",
            "end_time": "Thu, 22 Oct 2020 14:11:25 GMT",
            "id": 3,
            "modified_date": "Tue, 07 Jul 2020 14:58:25 GMT",
            "name": "Street Art",
            "start_time": "Thu, 22 Oct 2020 13:11:25 GMT"
        }
    ],
    "classrooms": [
        {
            "building": "Daniels",
            "created_date": "Thu, 18 Jun 2020 17:51:57 GMT",
            "floor": "4",
            "id": 1,
            "modified_date": "Thu, 18 Jun 2020 17:51:57 GMT",
            "name": "DLS427",
            "occupancy": 200
        }
    ],
    "success": true
}

POST '/lecture/add'
- Post a new lecture to the database
- Request: Arguments(required): Send a JSON object with key:value pairs of name, class_id, classroom_id, start_time (timestamp with timezone), end_time (timestamp with timezone).
- Authentication: JWT Bearer Token. Required permission: 'post:lecture'
Sample Request body:
{
	"name": "Wes Anderson Color Usage",
	"class_id": 10,
  "classroom_id": 2,
	"start_time": "2020-03-01 8:00:25-04",
	"end_time": "2020-03-01 8:59:25-04"
}

- Returns: an JSON object of the newly created lecture, the total number of lectures, along with a simple success message indication everything worked as expected.
{
    "new_lecture": [
        {
            "class_id": 10,
            "classroom_id": 2,
            "created_date": "Tue, 07 Jul 2020 23:44:32 GMT",
            "end_time": "Sun, 01 Mar 2020 12:59:25 GMT",
            "id": 17,
            "modified_date": "Tue, 07 Jul 2020 23:44:32 GMT",
            "name": "Wes Anderson Color Usage",
            "start_time": "Sun, 01 Mar 2020 12:00:25 GMT"
        }
    ],
    "success": true,
    "num_lectures": 12
}



PATCH '/lecture/<lecture_id>'
- Post a new lecture to the database
- Request: Arguments(required): Send a JSON object, with key:value pairs of name, class_id, classroom_id, start_time (timestamp with timezone), end_time (timestamp with timezone).
- Authentication: JWT Bearer Token. Required permission: 'post:lecture'
Sample Request:
http://localhost:5000/lecture/8
Sample Request body:
{
	"name": "Heart Anatomy 101",
	"class_id": 3,
    "classroom_id": 5,
	"start_time": "2020-11-22 11:10:25-04",
	"end_time": "2020-11-22 12:10:25-04"
}

- Returns: a JSON object of the updated lecture, along with a simple success message indication everything worked as expected.
{
    "lecture": [
        {
            "class_id": 3,
            "classroom_id": 5,
            "created_date": "Tue, 07 Jul 2020 20:51:42 GMT",
            "end_time": "Sun, 22 Nov 2020 16:10:25 GMT",
            "id": 8,
            "modified_date": "Wed, 08 Jul 2020 01:13:17 GMT",
            "name": "Heart Anatomy 101",
            "start_time": "Sun, 22 Nov 2020 15:10:25 GMT"
        }
    ],
    "success": true
}


DELETE '/lecture/<lecture_id>'
- Deletes lecture by lecture_id
- Request: Arguments: None
- Authentication: JWT Bearer Token. Required permission: 'delete:lecture'
- Returns: a JSON object of the deleted lecture id, the total number of lectures remaining, and a success message indicating that everything worked as expected. 
{
    "deleted_lecture": 16,
    "success": true,
    "num_lectures": 11
}


## Testing
To run the tests, using `test_app.py`, import your current JWT Bearer Token into the setup.sh file. Then in the backend directory, from terminal, run: 
```
source setup.sh
dropdb class_scheduler_test
createdb class_scheduler_test
psql class_scheduler_test < class_scheduler.psql
python3 test_app.py
```