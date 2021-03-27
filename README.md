# Django-starter

My Django Starter App

## Creating a virtual env and activate the virtual env
	\> py -m venv name_of_env
	
	\> cd name_of_env
	
	\name_of_env> cd Scripts
	
	...\name_of_env/Scripts> activate.bat
	
## Sarting a new Django Project 
	\> django-admin startproject project_name
	
## Running the new app	
	\> python migrate
	
	\> python manage.py createsuperuser --email youremail@mail.com --username admin
	
	\> python manage.py runserver	

	http://127.0.0.1:8000/
		
## Start a new app

	\> python manage.py	startapp app_name
	
**NB if you need a new project package**
	
Cd to Django-starter and run the command

	\> python remove_version.py
	
This will remove all the versions of the packages used create a new file name new_requirements.txt 

Run
	\> pip3 install -r requirements.txt
	
	OR
	
	\> pip3 install -r new_requirements.txt

	This will install all the necessary packages
	
**You are set to go**

To Generate requirements file, enter  the command below

\> pip freeze >> requirements.txt
