# SPOC - Single Point Of Control :vulcan_salute:

Backend repo for LACE ERP

## General requirements:

- Backend:
  - The server side of the app is running in `Python 3.9.8`.
- Gitflow:
  TBD

## Local Development:

### Pre-requisites

Make sure you have the correct version of python installed. It is recommended that you work with virtual environments, this will help you to manage the correct version of the dependencies that you are using in your project.

You can create a virtual environment with the next command:

```shell
# MacOs
python -m venv venv

#Windows
py -3 -m venv venv
```

or

```shell
python3 -m venv venv
```

and you need to initilize your environment:

```
# MacOs
. venv/bin/activate

# Windows
venv\Scripts\activate
```

After you have your virtual environment for the backend, you can install all the requirements needed for the app:

```
pip install -r app/requirements
```

Now that you have everything in place, you need to export the env variable and run the app:


### Environment variables

Create a `.env` inside the `app` directory, , use the `example.env` file to copy all the keys needed, and change the required values for the app to run, if you don't know any value please reach out to Rodrigo. With this you will be able to set up your local DB running.

### Local database

Please install [PostgreSQL v14](https://www.postgresql.org/download/) and create database. The credentials needed will be in the `.env` that any dev can share.

### Starting the local environment

You will need to install all the requirements

```shell script
pip install -r requirements.txt
```

After that, just run `python app/run_app.py` this will load the complete environment and start the local server.

### Black

Plase run [black](https://github.com/psf/black) on all your files:

```

python -m black .

```

### Pre-commit

Now you need to install the [pre-commit](https://pre-commit.com/index.html) hooks in order to clean the code clean, to do that please run:

```shell
pre-commit install
```

Now each time you commit a file, pre-commit will run and check your files, make sure all the hooks pass before you push your code.

Recommendation: Use pylint to lint your code, that will help to mantain the project.

### Code good practices

The idea of having best practices when coding is something that you need to define with your team and stick to those practices, but we can generalize some thigs for the backend.

Plase stick to follow [pep8](https://www.python.org/dev/peps/pep-0008/) when coding in python, this will help us to follow good standards when writing code.

### How to test

Let's follow the [test driven development (TDD)](https://en.wikipedia.org/wiki/Test-driven_development). Please make sure your tests are mocked up correctly and all the dependencies are managed automatically.

Each module should have their own tests, this will allow us to just worry about the part of the code we are changing.
Let's start working with the actual configuration:
```
mypkg/
    __init__.py
    code.py
    test/
        __init__.py
        test_code.py
        run_tests.py
        ...
```

## Dev Deployment:

TBD

## Needed tasks:

- Automated the complete flow, making the developer to forget about pylint, black and pre-commit.
- Automate and make easier the local development flow. Some ideas:
  - Create a script to spin up everything.
  - Use docker to create the complete app inside the containers.
- Make easier the way to set up a local DB and to populate some data. Some ideas:
  - We can create a shared DB in a development enviroment, let's see if we can connect and we will have a DBA.
  - We can create a docker file to spin up a container and create a seeder for the application.
- Dockerize the app???
