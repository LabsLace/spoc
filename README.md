# SPOC - Single Point Of Control :vulcan_salute:

Monorepo for the complete App needed for LACE.

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
pip install -r app/backend/requirements
```

Now that you have everything in place, you need to export the env variable and run the app:


### Environment variables

Create a `.env` inside the `app/backend` directory, , use the `example.env` file to copy all the keys needed, and change the required values for the app to run, if you don't know any value please reach out to Rodrigo. With this you will be able to set up your local DB running.

### Local database

Please install [PostgreSQL v14](https://www.postgresql.org/download/) and create database. The credentials needed will be in the `.env` that any dev can share.

### Starting the local environment

You will need to install the local web server:
```
pip install "uvicorn[standard]"
```

After that, just run `uvicorn --app-dir app/backend main:app --reload` this will load the complete environment and start the local server.

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
