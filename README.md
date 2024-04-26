# EM Field application (Frontend)

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/DekuMawuli/dj-api-con.git
$ cd dj-api-con
```

Create a virtual environment to install dependencies in and activate it:
Ensure that you have python (>=3.11.7) set up on machine

```sh
https://www.python.org/downloads/
$ python3 -m venv .venv
$ source env/bin/activate
```


Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `venv`.

Once `pip` has finished downloading the dependencies:
```sh
(venv)$ cd project
(venv)$ python manage.py migrate (Optional Though)
(venv)$ python manage.py runserver
```
And navigate to `http://localhost:8000`.
