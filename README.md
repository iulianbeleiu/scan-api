# django-base-api

#### Create a new project
```
Make sure app folder is created befor this command
sudo docker-compose run app sh -c "django-admin startproject app ."
```

#### Enable Travis CI
```
Go to https://travis-ci.org/ and enable the repository 
```

#### Create a new app
```
sudo docker-compose run app sh -c "python manage.py startapp app_name"
```

#### Make migrations
```
sudo docker-compose run app sh -c "python manage.py makemigrations"
```

#### Run Tests and flake8
```
sudo docker-compose run --rm app sh -c "python manage.py test && flake8"
```