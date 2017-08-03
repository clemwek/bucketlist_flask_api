[![Build Status](https://travis-ci.org/clemwek/bucketlist_flask_api.svg?branch=master)](https://travis-ci.org/clemwek/bucketlist_flask_api)

[![Build Status](https://travis-ci.org/clemwek/bucketlist_flask_api.svg?branch=master)](https://travis-ci.org/clemwek/bucketlist_flask_api)

# Bucketlist Flask API

What would you like to do in the next few years? Climb a mountain? Learn to ride a bike? :) 
It’s important to keep track of what you have already done and what you are yet to achieve. 
Register and start tracking.

## Installing

### Database setup

Install the postgres db, instructions [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)

create db

` $ createdb test_db`

`$ createdb flask_api`

### Project setup

Make sure you have python installed in your system if not visit [python](https://www.python.org/downloads/) and get a copy for your system

Clone the project

    `git clone https://github.com/clemwek/bucketlist_flask_api.git <foldername>`
    
Change Directory into the project folder

    `cd <foldername>`
    
Create a virtual environment with Python

   `$ virtualenv -p python3 <yourenvname>`
   
Activate the virtual environment

    `$ source <yourenvname>/bin/activate`
    
Install the application's dependencies from requirements.txt to the virtual environment

    `$ pip install -r requirements.txt`
    
Run the app on port 5000

    `python run.py`
