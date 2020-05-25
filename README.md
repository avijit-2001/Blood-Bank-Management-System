# Guidelines for Running codes
Install the following dependencies [in linux] for running the project
. First go the directory where project is extracted. i.e BloodBank/

On executing 
## Installation

1. Install python virtual environment


```bash
python -m pip install --user virtualenv
```

2. Go to the directory where project is saved and create a new virtual environment new_v using the following command:

```bash
python3 -m venv new_v
```

3. Activate the virtual environment

```bash
source new_v/bin/activate
```
4.Install django and django-crispy-forms

```bash
pip install django
pip install django-crispy-forms
```
5. Execute the following command to run the server:
```bash
python manage.py runserver
```
5. Open the following address in your browser
```bash
http://127.0.0.1:8000/
```
