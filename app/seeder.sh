#!/bin/sh
rm db.*
rm */migrations -r 
python3 manage.py makemigrations users
python3 manage.py migrate
python3 manage.py shell < z-c-der/seeder.py
