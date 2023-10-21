Project name:
Test work at "wht.agency" company

Project description:

This project is an API application. Users can edit their own profile, including avatar, create teams and manage their employees. Implemented social authentication using Google and Facebook, regular registration, registration with account activation via email, username and password reset via email. The project is built using the Django REST Framework (DRF) for the API.

Development Tools:

    Python >= 3.11
    
    Django == 4.2.6
    Django REST Framework 3.14.0

    Docker


Installation and running the project:

1) Clone the repository

       https://github.com/Costello90/t_w_wht_agency.git
2) Create a virtual environment

       cd t_w_wht_agency
       python -m venv venv

3) Activate virtual environment

   Linux

       source venv/bin/activate

   Windows

       ./venv/Scripts/activate
4) Install dependencies:

       pip install -r requirements.txt
5) In the root directory of the project, create an ".env" file. In the ".env" file, copy all the variables from the ".env.sample" file and give them values
6) Run tests

       python manage.py test
7) Create migrations

       python manage.py makemigrations
8) Apply migrations to the database

       python manage.py migrate
9) Run server

       python manage.py runserver
10) For social authorization to work, you need to obtain your own CLIENT_SECRET and CLIENT_ID on the Google and Facebook platforms and fill out the ".env" file
       
       Endpoints for testing (for Facebook you need to use only "localhost"):

        http://localhost:8000/auth/o/google-oauth2/?redirect_uri=http://localhost:8000/auth/o/google-oauth2/
        http://localhost:8000/auth/o/facebook/?redirect_uri=http://localhost:8000/auth/o/facebook/ 
11) Links

    DRF API 

        http://127.0.0.1:8000/


Deploying the application using Docker:

1) Ensure that Docker and Docker Compose are installed on your system.

2) In the root directory of the project, create an ".env" file. In the ".env" file, copy all the variables from the ".env.sample" file and give them values

3) Build the Docker images:

       docker-compose build
4) Start the containers:

       docker-compose up
5) You can now open a web browser and see the application in action at the following address.
       
       http://127.0.0.1:8000
6) If you need to run the tests yourself, you need to run the commands:
       
       docker-compose up
       docker container ls
   You need to copy the ID of the running container with our application and paste it instead of "<container_id>"

       docker exec -it <container_id> /bin/bash
       python manage.py test

License:

Copyright (c) 2023-present, Kostiantyn Kondratenko
