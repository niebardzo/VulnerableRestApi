from flask import Flask, jsonify, abort, make_response, request, render_template
import json
import csv
from lxml import etree

def read_csv(file):
	fieldnames = ['id' ,'Name', 'Owner', 'Breed']
	database = []
	with open(file, 'r') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames=fieldnames)
		for row in reader:
			database.append(row)
		return database


def write_csv(file, data):
	name, owner, breed = data
	database = read_csv(file)
	fieldnames = ['id' ,'Name', 'Owner', 'Breed']
	with open(file, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		for row in database:
			writer.writerow({'id': row['id'] ,'Name': row['Name'], 'Owner': row['Owner'], 'Breed': row['Breed']})
		writer.writerow({'id': len(database)+2 ,'Name': name ,'Owner': owner, 'Breed': breed})
	return str(len(database)+2)




app = Flask(__name__)


@app.route("/api/v2/dog/<num>", methods=['GET', 'FAKE'])
def get_dog(num):
	if request.method == 'GET':
		database = read_csv('database.csv')
		for row in database:
			if row['id'] == num:
				resp = make_response(jsonify(row), 200)
				break
			else:
				resp = make_response(jsonify({'Message': 'Dog does not exist'}), 404)
		return resp
	if request.method == 'FAKE':
		resp = make_response(jsonify({'Message': 'Keep trying, look for docs.'}), 405)
		return resp


@app.route("/api/v2/dog", methods=['GET','POST', 'PUT', 'UPLOAD' ])
def add_dog():
	if request.method in ['POST', 'PUT', 'UPLOAD']:
		#CREDS: security:wholetthedogsout
		if request.headers.get('Authorization') == 'Basic c2VjdXJpdHk6d2hvbGV0dGhlZG9nc291dA==':
			if request.headers.get('Content-Type') == 'application/json':
				try:
					doc = request.json
					to_add = (doc['Name'], doc['Owner'], doc['Breed'])
					dog_id = write_csv('database.csv', to_add)
					resp = make_response(jsonify({'Message': 'Dog {} added to the database with id: {}'.format(doc['Name'], dog_id)}), 200)
					return resp
				except (json.decoder.JSONDecodeError, KeyError) as e:
					resp = make_response(jsonify({'Message': 'Json wrongly formatted. Please refer to the docs.'}), 415)
					return resp
			if request.headers.get('Content-Type') in ['application/xml', 'text/xml']:
				try:
					xml = request.data
					parser = etree.XMLParser(no_network=False, dtd_validation=False)
					doc = etree.fromstring(xml, parser)
					name = doc.find('name').text
					owner = doc.find('owner').text
					breed = doc.find('breed').text
					to_add = (name, owner, breed)
					dog_id = write_csv('database.csv', to_add)

					parsed_xml = '<root><message>Dog {} added to the database with id: {}</message></root>'.format(name, dog_id)

					resp = make_response(parsed_xml, 200)
					resp.headers['Content-Type'] = 'application/xml'
					return resp	
				except:
					resp = make_response(jsonify({'Message': 'Unsupported Content-Type.'}), 415)
					return resp
			else:
				resp = make_response(jsonify({'Message': 'Content-Type must be set to application/json'}), 415)
				return resp
		else:
			resp = make_response(jsonify({'Message': 'Unauthorized'}), 401)
			return resp


	if request.method == 'GET':
		if str(request.headers.get('X-HTTP-METHOD')).upper() in ['POST', 'PUT', 'UPLOAD'] or str(request.args.get('_method')).upper() in ['POST', 'PUT', 'UPLOAD']:	
			if request.headers.get('Content-Type') == 'application/json':
				try:
					doc = request.json
					to_add = (doc['Name'], doc['Owner'], doc['Breed'])
					dog_id = write_csv('database.csv', to_add)
					resp = make_response(jsonify({'Message': 'Dog {} added to the database with id: {}'.format(doc['Name'], dog_id)}), 200)
					return resp
				except (json.decoder.JSONDecodeError, KeyError) as e:
					resp = make_response(jsonify({'Message': 'Json wrongly formatted. Please refer to the docs.'}), 415)
					return resp
			if request.headers.get('Content-Type') in ['application/xml', 'text/xml']:
				try:
					xml = request.data
					parser = etree.XMLParser(no_network=False, dtd_validation=False)
					doc = etree.fromstring(xml, parser)
					name = doc.find('name').text
					owner = doc.find('owner').text
					breed = doc.find('breed').text
					to_add = (name, owner, breed)
					dog_id = write_csv('database.csv', to_add)

					parsed_xml = '<root><message>Dog {} added to the database with id: {}</message></root>'.format(name, dog_id)

					resp = make_response(parsed_xml, 200)
					resp.headers['Content-Type'] = 'application/xml'
					return resp	
				except:
					resp = make_response(jsonify({'Message': 'Unsupported Content-Type.'}), 415)
					return resp
			else:
				resp = make_response(jsonify({'Message': 'Content-Type must be set to application/json'}), 415)
				return resp
		else:
			resp = make_response(jsonify({'Message':'Please specify the dog id to view the dogs. Please refer to the documentation'}), 200)
			return resp




@app.route("/api/v2/docs", methods=['GET, '])
def docs_v2():
	return 'KUPA'

@app.route("/api/docs", methods=['GET, '])
def docs():
	return 'KUPA'

if __name__ == '__main__':
	print("Starting python app")
	app.run(host='0.0.0.0', debug=False)
