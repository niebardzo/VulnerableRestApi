# VulnerableRestApi

The project contains the flask webserver with vulnerable Rest API - the API is vulnarable to XXE which allows the SSRF and Local Storage Reading. Then there is localserver which allows the remote code execution.

## HOW TO SET UP

Move the project to /var/www/html/python, if the dir does not exist, create one.

Using pipenv install all the dependecies.

```
pipenv install --dev
pipenv shell
```

Then to set up the whole lab, please: start the localserver.py on localhost with the command:

```
python localserver.py
```

To give the attacker the hint where the local server is create the user with the basedir of localserver.py

```
sudo useradd -b /var/www/html/python/localserver.py python_server
```

Then run the final server using the gunicorn cgi and nginx as reverse proxy. The nginx configuration can be found here:

https://docs.gunicorn.org/en/latest/deploy.html

By default the gunicorn runs on localhost:8000, so change the proxy_pass to locahost:8000, then restart the nginx and run the gunicorn with below command:

```
gunicorn wsgi:app
```

Then you are ready to go.


## Task

1. Exploit the XXE
2. Read /etc/passwd on the attacked machine
3. Find the service listening on localhost
4. Get the reverse shell. (RCE)

## Security

Please do not run this software on the production or untrusted network under no circumstances.