# Social Apps 

Api's For social networking application 


## Installation

For all the installation steps python in must be installed in your system 

Create Virtual env 

```bash
python3 -m venv env 

source env bin activate                    # for activating the env
```

### Requirements

```python
# Requirement file is exists in project dir 

## Run the command for install the requirements

pip install -r requirements.txt

```

## Database

After successfully install all requirements you need to provide database cred. from .env
I used postgresql database for this project . you can use sqllite3 also i comment it out that in setting.py


## Migrate

```python
# After connected database you need to run migrate command for migrating database

 python manage.py migrate 
```
## RUN Server 

```python
# After migrate you need to run the command for server start

python manage.py runserver 

```

### Api Check 

For the api i include the postman collection with project you need to import that in postman and also implement the swagger for better understanding below i mention swagger url :- 

```
http://localhost:8000/api/swagger
```  
## Docker 

For docker i take some help from internat and take some things from myself. yes i used docker and worked on it in my previous company so i know about the docker and some basics. 

I Create Docker file for the setup and configure the project and create docker-compose.yaml file for configure the services and provide the dependency of postgres database and provide the database service and project running command.

## Note :- 

I used API View in this project for more customise the code and api formate and provide JWT authentication simplejwt package .
According the project and based on your architecture i can also use multiple views like Generic View, Model View set etc.

Also databse schema is atteched with project.


# Thanks and Regards

```
Ashutosh Sharma :)
```
