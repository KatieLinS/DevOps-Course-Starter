# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before poetry will be recognised.**

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). 

Please update the following variables:

- [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.
- [MONGOBD_PRIMARY_CONNECTION_STRING](https://portal.azure.com/#@devops.corndel.com/resource/subscriptions/d33b95c7-af3c-4247-9661-aa96d47fccc0/resourceGroups/cohort32-33_KatLin_ProjectExercise/providers/Microsoft.DocumentDB/databaseAccounts/katlin-cosmosdb/Connection%20strings) variable which is used for connecting to MongoDB.


## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app 'todo_app/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the test

### In a terminal

Run `poetry run pytest` to run the tests

### In VS Code 

(make sure you have python extension installed)
- click on the Flask icon on the left bar
- click `Configure Python Tests`
- choose `pytest`
- select a folder (`root` or `todo app`)

## Hosting To-Do app on Virtual Machines using Ansible

### Prerequisite

Using `ssh-copy-id USERNAME@IP-ADDRESS`,
- Add your machine's public SSH keys to the Control Node 
- Add the Control Node's public SSH keys to all the Managed Nodes

(Run `ssh-keygen` to generate an SSH key pair if the machine doesn't already have one.)

### Deployment

- copy the `ansible` folder to the Control Node (You can use a command similar to the following line)

    ```bash
    scp -r /path/to/folder/ansible  USERNAME@IP-ADDRESS:/path/to/copy
    ```    
- run the following command to deploy the app on Managed Nodes
    
    ```bash
    ansible-playbook ./ansible/my-ansible-playbook.yml -i ./ansible/my-ansible-inventory 
    ```
    (You will be prompted to provide the PRIMARY CONNECTION STRING for MongoDB)

## Building and running development, production and test containers in Docker
### Development

Please run ```docker compose up``` to build and run the container for development 

Alternatively, you can build the container with the command below
```bash
docker build --target development --tag todo-app:dev .
``` 

and run the container with the command below
```bash
docker run --env-file .env --publish 5001:5000 -it --mount "type=bind,source=$(pwd)/todo_app,target=/todo_app" todo-app:dev
```

### Production

For building the container
```bash
docker build --target production --tag todo-app:prod .
```

For running the container

```bash
docker run --env-file .env --publish 5001:5000 -it todo-app:prod
```

### Test

For building the container
```bash
docker build --target test --tag todo-app:test .
```

For running the container

```bash
docker run todo-app:test
```

## Hosting the container image on DockerHub
### Login to docker 
```bash
docker login
```
### Build and push the image onto Docker Hub
```bash
docker build --target production --tag katielht/todo-app:prod .  
docker push katielht/todo-app:prod                                                              
```
Add `--platform=linux/amd64` to the build command if you are building on a Mac M1.

The image of the todo app is deployed to DockerHub at https://hub.docker.com/repository/docker/katielht/todo-app/general 


## Host the frontend on Azure Web App
The todo app is created and hosted on https://katlin-todo-app.azurewebsites.net/ 

To update the app, rebuild and push the image to Docker Hub, and run `curl -v -X POST '<webhook>'` or make a POST request to the webhook in Thunder Client in VSCode. You can find the webhook under Deployment Center on the app service’s page in the Azure portal.