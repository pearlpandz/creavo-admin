venv
----
python -m venv <environment_name>
<environment_name>\Scripts\activate

python
------
pip freeze > requirements.txt
pip install -r requirements.txt

docker
------
docker run -d --name postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=creavo -p 5432:5432 -v pgdata:/var/lib/postgresql/data postgres:14

django
------
python -m pip install django
django-admin startproject app_name project_name
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


How to start the local server
> .django\Scripts\activate
> python manage.py runserver