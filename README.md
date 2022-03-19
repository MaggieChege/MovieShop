# MovieShop
Django API for an online movie shop

# Setup
1.Install virtualenv using `pip3 sudo pip3 install virtualenv`

2.Create a virtual environment virtualenv venv

Activate your virtual environment: `source venv/bin/activate`

3.Clone this repo 
`https://github.com/MaggieChege/MovieShop.git`

4.Install all the dependancies in the requirements.txt file `pip install -r requirements.txt`

5.Use instructions on `create_db.sql` to CREATE DB

6.Create a .env file in the project folder and and the following exports:

    export DATABASE="<name of your database>"
    export PASSWORD=<password>
    export USER="<your postgres username>"

7.Export the settings by running the command: `source .env`

8.Migrate the database:

`python manage.py makemigrations`


`python manage.py migrate`

9.Run the server:

`python manage.py runserver`


10.Create superUser
`python manage.py createsuperuser`

11.Available endpoints are Documented using Swagger on `http://127.0.0.1:8000/docs/`

