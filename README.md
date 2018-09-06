
# Coding-With-Seniors

This website helps in organising and documenting the Coding With Seniors sessions conducted yearly by the Computer Science and Engineering Association, NIT Calicut.

  

## Features

- Create events and sessions. Add reading materials, problems, leaderboard for every session.

- Have an internal rating system within NITC which can be updated after every session allowing top_coder and top_improver to be selected upon this.

- Users can post editorials for the problems on the contests and based on the likes recieved for an editorial, top_contributor is selected for every session.

- Users can link their coding accounts to their accounts and have a userprofile on the site.

  

## Getting Started

  

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

  

### Prerequisites

Anaconda and python 3

  

### Installing

Clone the repository

```

git clone https://github.com/csea-nitc/Coding-With-Seniors.git

```

Navigate to the folder

  

Activate your environment in anaconda or choose to start a virtual environment of your choice.

```

conda activate {env_name}

```

Install the requirements

```

pip install -r /path/to/requirements.txt

```

  
Setup the database 
```

python manage.py makemigrations

python manage.py migrate

python manage.py migrate --run-syncdb
```
Create superuser and runserver
```
python manage.py createsuperuser

python manage.py runserver

```

  

### First thing to do after setting up the local server

Navigate to 127.0.0.1:8000/admin and create a user_profile for the admin else the leaderboard will not work.

  

Happy Coding

  

## Deployment

  

I am not going to run you through the deployment on heroku if you really wanna deploy it, you better try and set it up on a new app and experiment with the setup.

  

There are two environment variables.

- DEBUG

- SECRET_KEY

  

### Maintaining

Heroku is closely integrated with git.

We are using postgreSQL on heroku and our website will be run on one of their dynos.

  

Pushing any modified changes to the CWS site.

```

git remote add origin https://github.com/csea-nitc/Coding-With-Seniors.git

git remote add heroku https://git.heroku.com/cws-nitc.git

git pull origin master

git push heroku master

heroku open

```

This will change the appearance or the logic but will not affect the database on Heroku.

  

For applying Database changes. 
Setup the CSEA and heroku remote as in previous step and....

```

heroku run python manage.py makemigrations

heroku run python manage.py migrate

heroku run python manage.py migrate --run-syncdb

heroku open

```

  

To reset the entire database

```

heroku pg:reset DATABASE

```

Now you will have to follow the steps in applying the database changes and create a superuser as in the local deployment followed by creating their user_profile in admin console.

  
  

## Scope for Future Improvement

- The dyno on Heroku will sleep and heroku will assign the dyno to some other application within their environment if there is an inactivity of 30 minutes. This does not affect the hosting of our website but will result in a 2-3 secong load time for rebuilding our dynos after a session of inactivity. Try to find altenartive hosting services or set it up on our new servers if possible.

- The site has CSS and bootstrap problem with chrome.

- There can be a lot of features that you can add to the site if you actually brainstorm.

	- Maybe be use a webscraper to go to codeforces and update the users about upcoming contests etc.
