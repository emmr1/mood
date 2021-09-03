# Environment
Developed in WSL: Ubuntu-20.04 with Django and Django Rest Framework
Follow WSL install instructions here: https://code.visualstudio.com/docs/remote/wsl

## Set up virtual env
Set up a virtual environment within the root of the project
```
python3 -m venv venv
source venv/bin/activate
```

## Install dependencies
Ensure you have pip installed
In the project directory run `pip3 install -r requirements.txt`


# Db set up
```
python manage.py makemigrations moodapp
python manage.py migrate
python manage.py createsuperuser --email <youremail> --username admin
```

# Run the server locally
```
python manage.py runserver
```

# Add users
Navigate to http://127.0.0.1:8000/admin/ to create users and manage their permissions

# Changes to make production-ready
- Containerize
```
# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
```

- Instead of sqlite database, configure independent postgres or mysql cluster on the cloud (e.g. AWS RDS or Cloud SQL)
- Use a dedicated identify provider for authentication (e.g. Okta) 
- Set up CI/CD pipeline with dev test and prod environments
- Write test cases (test driven dev), ensure high code coverage
- Do a security/threat analysis (e.g. OWASP top 10)
- Get SSL cert, including automatic revocation and renewal
- Deploy to cloud, highly available with load balancer and container orchestration in multiple availability zones, ensure auto-scaling is configured and load-tested.


