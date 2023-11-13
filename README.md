## Overview : wrestling-gram-backend

Backend for the [WrestlingGram](https://github.com/fra-zelada/wrestlingGram) project, created in **Python** with **Django Rest Framework**, providing user authentication, session management with **HttpOnly** refresh tokens, image uploading with **Cloudinary**, and creation of posts and comments.
## Quick Start Guide

### Clone the Repository:

```
git clone https://github.com/fra-zelada/drf_blog.git
<<<<<<< HEAD
cd drf_blog
=======
```

### Set Up a Virtual Environment:

```
>>>>>>> origin/main
py -m venv venv
```

### Activate the Virtual Environment:

```
.\venv\Scripts\activate
```

### Install Dependencies:

```
pip install -r requirements.txt
```

### Create Database Migrations:

```
python manage.py makemigrations

```

### Apply Migrations:

```
python manage.py migrate

```

### Configure Environment Variables

Note: Obtain your Cloudinary API key, API secret, and cloud name from your Cloudinary account.

Rename the file ```.env.TEMPLATE``` to ```.env```
Open the ```.env``` file and configure the following environment variables:

```
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
CLOUDINARY_CLOUD_NAME=CLOUD_NAME
CLOUDINARY_API_KEY=API_KEY
CLOUDINARY_API_SECRET=API_SECRET
```

### Run the Development Server:

```
python manage.py runserver
```

Now, your Django app should be up and running. Open your browser and navigate to http://127.0.0.1:8000/ to see your application in action.


### Note: Updating the Project on PythonAnywhere


Activate the virtual environment in the console

```
source .virtualenvs/venv/bin/activate
```

Perform migrations

```
python manage.py makemigrations
python manage.py migrate
```

Backup the ```settings.py``` file

Discard all local changes and overwrite with the remote version
```
git reset --hard HEAD
```

Pull the latest version from the remote repository
```
git pull
```

Manually modify ```settings.py```, adding production database details




