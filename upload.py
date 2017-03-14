import requests
import sys
import os
import uuid
import json
import argparse

# may need to escape file names in some way, not sure...
def content_disposition(filename):
	return 'attachment; filename="' + filename + '"'


# per http://docs.overviewproject.apiary.io/#reference/files/file/upload-file?console=1
def upload_single_file(server_url, api_token, filename):
	url = server_url + '/api/v1/files/' + str(uuid.uuid4())

	headers = { 'content-disposition' : content_disposition(filename),
				'content-length' : str(os.path.getsize(filename)) }

	file = open(filename, 'rb')

	r = requests.post(url, auth=(api_token,'x-auth-token'), headers=headers, data=file.read())
	r.raise_for_status()


# per http://docs.overviewproject.apiary.io/#reference/files/finish-uploading-files/add-files-to-document-set?console=1
def finish_upload(server_url, api_token):
	url = server_url + '/api/v1/files/finish'
	headers = {'Content-Type':'application/json'}
	data = { 'lang' : 'en' }

	r = requests.post(url, auth=(api_token,'x-auth-token'), headers=headers, data=json.dumps(data))
	r.raise_for_status()


# ---- Main ----

parser = argparse.ArgumentParser(description='Upload a file or directory to an Overview server.')
parser.add_argument('file', help='file or directory to upload')
parser.add_argument('-t', '--token', help='API token corresponding to document set', required=True)
parser.add_argument('-s', '--server', help='url of Overview server, defaults to http://localhost:9000', default='http://localhost:9000')
args = parser.parse_args()

upload_single_file(args.server, args.token, args.file)
finish_upload(args.server, args.token,)



