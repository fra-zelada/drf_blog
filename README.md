git clone https://github.com/fra-zelada/drf_blog.git
py -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt
python manage.py makemigrations

pip install django

django-admin startproject miniblog .

manage.py startapp post ./miniblog/post

manage.py runserver

pip install djangorestframework

manage.py makemigrations
manage.py migrate
python manage.py createsuperuser --username admin --email admin@example.com


curl -X POST -H "Content-Type: application/json" -d "{\"username\": \"admin\", \"password\": \"123456\"}" https://127.0.0.1:8000/api/token/

curl -X GET http://127.0.0.1:8000/api/post/1/ -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzODQ0NDY2LCJpYXQiOjE2OTM4NDQxNjYsImp0aSI6Ijk0NGM5NmZjM2Q5NTQxYTY4ZTExZDUzNzkwMjNjMjA0IiwidXNlcl9pZCI6MX0.H5qFcrNWYrgzJ0jifFSHJI7nVjyAhLt7LxNqtgT1PuM"



openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

SECURE_SSL_CERTIFICATE = 'tu_proyecto/ssl/cert.pem'
SECURE_SSL_KEY = 'tu_proyecto/ssl/key.pem'

manage.py runsslserver

source .virtualenvs/venv/bin/activate
hacer migraciones
# Descarta todos los cambios locales y sobrescribe con la versión remota
(venv) 03:02 ~/drf_blog (main)$ git reset --hard HEAD

# Realiza el pull para obtener la versión más reciente desde el repositorio remoto
(venv) 03:02 ~/drf_blog (main)$ git pull