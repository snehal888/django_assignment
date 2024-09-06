# django_assignment

* Create an virtual Environment:-
  python -m venv myenv
* Creating a new project:-
  django-admin startproject configuration .
* Creating new app:-(setup, social_network)
  django-admin startapp setup
  django-admin startapp social_network
* Activate virtual environment:-
  myenv\Scripts\activate
* Install Python and djangorestframework:-
  pip install djangorestframework
* Install Authentication(Simple JWT Authentication):-
  pip install djangorestframework-simplejwt
* Make database migrations:-
  py manage.py makemigrations
  py manage.py migrate
* Rus the server:-
  py manage.py runserver
* Add requirements.txt:-
  pip freeze > requirements.txt
