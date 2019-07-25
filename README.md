# VulnerableRestApi

The project contains the flask webserver with vulnerable Rest API - the API is vulnerable to XXE which allows the SSRF and Local Storage Reading. Then there is a local server which allows the remote code execution.

## HOW TO SET UP

Move the project to /var/www/HTML/python, if the dir does not exist, create one.

To give the attacker the hint where the local server creates the user with the based of localserver.py

```
sudo useradd -b /var/www/html/python/ localserver.py
```

Create the user that is going to run the webservers.

```
sudo useradd webserver
mkdir /home/webserver
mkdir /var/www/html/python
chown webserver /home/webserver
chown webserver /var/www/html/python
su webserver
```

Using pipenv install all the dependencies.

```
pipenv install --dev
pipenv shell
```

Then to set up the whole lab, please: start the localserver.py on localhost with the command:

```
python localserver.py
```


Then run the final server using the gunicorn CGI and Nginx as a reverse proxy. The Nginx configuration can be found here:

https://docs.gunicorn.org/en/latest/deploy.html

By default, the gunicorn runs on localhost:8000.

```
gunicorn wsgi:app
```

Or for the testing purpose, you could run the gunicorn to listen everywhere running on the user webserver.

```
gunicorn --bind 0.0.0.0:8888 wsgi:app
```

Then you are ready to go.


## Task

1. Exploit the XXE
2. Read /etc/passwd on the attacked machine
3. Find the service listening on localhost
4. Get the reverse shell. (RCE)

## Security

Please do not run this software on the production or untrusted network under no circumstances.
