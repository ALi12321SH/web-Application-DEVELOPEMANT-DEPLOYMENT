This project is a user profile web application developed and deployed as part of a network course at Isfahan University of Technology. The project involves creating a web interface for user registration, login, profile management, and deploying it using a proxy server.


## Introduction

In this project, we develop and implement a website that displays user profiles. We then access it using a custom proxy server. The recommended backend language is Flask (a Python web framework), and for the frontend and HTML and  CSS are used.

## Features

- User registration with details
- User login
- Profile management (view and update profile information)
- Home page displaying a list of all users with their emails
- Account deletion feature

## Architecture

The project uses a minimum of three hosts within a NAT network:

1. **Host 1**: Hosts the website, database, and web server.
2. **Host 2**: Implements the proxy server, acting as an intermediary between Host 1 and Host 3.
3. **Host 3**: Client host that browses the website hosted on Host 1 through the proxy server.

## Installation

### Setting up the Development Environment

1. Create a Python virtual environment:

       virtualenv venv
       source venv/bin/activate

2. Install the required packages:

        pip install -r requirements.txt
  
3. Configure the database:
Install MySQL server:

        sudo apt-get install mysql-server
  
#### Execute the provided SQL script to set up the database and tables:

    mysql -u yourusername -p yourpassword 

    mysql> source \path\to\tconfig.sql;

4. Modify the app.py configuration:

        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'password'
        app.config['MYSQL_DB'] = 'profileApp'
5. Run the Flask application:

        flask run


## Deployment
### For deployment, we use NGINX and Gunicorn:

  1. Install NGINX and Gunicorn:
  
    sudo apt update
    sudo apt install nginx
    pip install gunicorn
  2. Run Gunicorn:

    gunicorn --bind 0.0.0.0:8000 app:app
  3. Configure NGINX: Create a new configuration file for NGINX:

    sudo nano /etc/nginx/sites-available/flask_app

    
  #### Add the following configuration:

    server {
        listen 80;
        server_name your_domain_or_IP;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/app/static;
    }
    }  
  #### Activate the configuration:

    sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled
    sudo nginx -t
    sudo systemctl restart nginx





## Contributing
If you wish to contribute to this project, please fork the repository and create a pull request with your changes.





   
