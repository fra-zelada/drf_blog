git clone https://github.com/fra-zelada/drf_blog.git
py -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

python manage.py runserver


source .virtualenvs/venv/bin/activate

hacer migraciones
# Descarta todos los cambios locales y sobrescribe con la versión remota
git reset --hard HEAD

# Realiza el pull para obtener la versión más reciente desde el repositorio remoto
git pull