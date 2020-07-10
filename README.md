# Class Scheduler Booking App

## Udacity Full Stack Nanodegree - Capstone Project

In Tech Ed, we are always advancing technology to provide school faculty and instructors to better utilize resources. We have created a booking application that enables faculty members to manage all lecture bookings and classrooms, as well as instructors of classes to search for available classrooms, create new lectures, update existing lectures, and delete their lectures.

### Backend

The `./backend` directory contains a Flask server with a SQLAlchemy module running on PostgreSQL. Required endpoints are found in `app.py`, database models in `models.py`, environment variables and required JWT tokens are contained in a bash file `setup.sh`, and this has been configured using Auth0 Authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

There is no frontend, yet! We are working on it! Soon there will be a `./frontend` directory containing a React frontend to consume the data from the Flask server. This will configure the Auth0 permissions and pass the JWT to the backend. 

The `/search` endpoint will show a calendar that will be popolated with all the lecture bookings available for the given date. The calendar will populate time slots and the selection will post to the `/lecture/add` endpoint. 

An instructor can then patch or delete their own lecture by clicking on a lecture they've created. The faculty member has full permissions to get, post, patch, delete all lectures created by anyone. The instructor can also access their own bookings under "my bookings" and access the `/instructor/<instructor_id>/lecture` endpoint, and a faculty member would see a tab called, "all bookings" where they could see a list of all bookings. 

We hope to have this complete, but this little bit of information should hopefully enable you to see the full potential of this API, and what we have in mind for it.

### Deployment

This project is deployed on Heroku using the `setup.sh` bash file. 
