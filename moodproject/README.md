# Environment
Developed in WSL: Ubuntu-20.04 with Django and Django Rest Framework
Follow WSL install instructions here: https://code.visualstudio.com/docs/remote/wsl

# Set up virtual env
Set up a virtual environment within the root of the project
```
python3 -m venv venv
source venv/bin/activate
```

# Install dependencies
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

# 

