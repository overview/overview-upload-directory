import requests
import sys
import os
import uuid
import json
import argparse
import hashlib

files_uploaded = 0

# check if a file is already on the server, via sha1 hash
def file_already_on_server(server_url, api_token, bytes):
	sha1 = hashlib.sha1(bytes).hexdigest()
	url = server_url + '/api/v1/document-sets/files/' + sha1
	r = requests.head(url, auth=(api_token,'x-auth-token'))

	return r.status_code == 204  # 204 = already got it, 404 = don't got it


# may need to escape file names in some way, not sure...
def content_disposition(filename):
	return 'attachment; filename="' + filename + '"'

# per http://docs.overviewproject.apiary.io/#reference/files/file/upload-file?console=1
def upload_single_file(server_url, api_token, filename, skip_existing=False):
	global files_uploaded

	bytes = open(filename, 'rb').read()

	if skip_existing and file_already_on_server(server_url, api_token, bytes):
		print(filename + " already on server, skipping")
		return
	else:
		print("Uploading " + filename + "...")

	url = server_url + '/api/v1/files/' + str(uuid.uuid4())

	headers = { 'content-disposition' : content_disposition(filename),
				'content-length' : str(os.path.getsize(filename)) }

	r = requests.post(url, auth=(api_token,'x-auth-token'), headers=headers, data=bytes)
	r.raise_for_status()
	files_uploaded += 1


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
parser.add_argument('-n', '--noskip', help='Don\'t skip documents already in this document set', action="store_true")
args = parser.parse_args()

upload_single_file(args.server, args.token, args.file, skip_existing=not args.noskip)
if files_uploaded > 0:
	finish_upload(args.server, args.token,)



