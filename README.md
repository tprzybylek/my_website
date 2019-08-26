# my_website

This is my personal website built with Wagtail. Wagtail is a Python CMS.

## Installation

Create a virtual environment and install required packages using pip.

```bash
$ python -m venv /venv
$ source venv/bin/activate
$ (venv) pip install -r requirements.txt
```

Create a database and start a development server

```bash
$ (venv) python manage.py makemigrations
$ (venv) python manage.py migrate
$ (venv) python manage.py runserver
```

## License
[MIT](https://choosealicense.com/licenses/mit/)