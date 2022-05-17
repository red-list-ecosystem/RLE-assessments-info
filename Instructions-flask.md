# Fireveg webapp based on Python/flask

## Documentation

This version has been developed following steps in
https://flask.palletsprojects.com/en/2.0.x/tutorial/

### Set up

Create a virtual environment for flask with miniconda:

```sh
conda create --name flsk
conda activate flsk
```

Update and install modules
```sh
/usr/local/opt/python@3.9/bin/python3.9 -m pip install --upgrade pip
pip3 install Flask
pip install psycopg2-binary
pip install flask-wtf
pip install folium
pip install pandas
```

Create and initialise directory
```sh
mkdir -p ~/proyectos/IUCN-RLE/RLE-assessments-info
cd ~/proyectos/IUCN-RLE/RLE-assessments-info
git init
```

```sh
pip freeze > requirements.txt
```

### Test the app

```sh
cd ~/proyectos/IUCN-RLE/RLE-assessments-info
export FLASK_APP=webapp
export FLASK_ENV=development
flask run
```

Initialise the database:

```sh
cd ~/proyectos/IUCN-RLE/RLE-assessments-info
export FLASK_APP=webapp
export FLASK_ENV=development
flask init-db
```

### Running with gunicorn

```sh
pip install gunicorn
cd ~/proyectos/IUCN-RLE/RLE-assessments-info
gunicorn -w 4 --reload --bind 0.0.0.0:5000 "webapp:create_app()"
```

### Other on-line resources

https://python-adv-web-apps.readthedocs.io/en/latest/flask.html

https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application
