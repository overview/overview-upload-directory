import requests
import sys
import os
import uuid
import json

API_TOKEN='8kr2sb7qgd4lh30crvg0rgttv'
SERVER_URL='http://localhost:9000'

def content_disposition(filename):
	return 'attachment; filename="' + filename + '"'


def upload_single_file(server_url, api_token, filename):
	url = server_url + '/api/v1/files/' + str(uuid.uuid4())

	headers = { 'content-disposition' : content_disposition(filename),
				'content-length' : str(os.path.getsize(filename)) }

	file = open(filename, 'rb')

	r = requests.post(url, auth=(api_token,'x-auth-token'), headers=headers, data=file.read())
	r.raise_for_status()


def finish_upload(server_url, api_token):
	url = server_url + '/api/v1/files/finish'
	headers = {'Content-Type':'application/json'}
	data = { 'lang' : 'en' }

	r = requests.post(url, auth=(api_token,'x-auth-token'), headers=headers, data=json.dumps(data))
	r.raise_for_status()

# ---- Main ----
if len(sys.argv) < 2:
	print("Usage: overview-upload [file or directory]")
	sys.exit(0)

file = sys.argv[1]

upload_single_file(SERVER_URL, API_TOKEN, file)
finish_upload(SERVER_URL, API_TOKEN)



