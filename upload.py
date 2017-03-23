#!/usr/bin/env python3
# Upload a file, or directory, to an Overview server. 
# From https://github.com/overview/overview-upload-directory
import requests
import sys
import os
import uuid
import json
import argparse
import hashlib
import traceback
import rfc6266

files_uploaded = 0

# Can Overview read this file? Basically just blacklists common formats we know we can't handle (yet)
def file_readable_by_overview(filename):
	path, ext = os.path.splitext(filename)
	return ext not in ['.zip', '.msg', '.gif', '.jpg', '.png', '.tiff', '.tif']


# check if a file is already on the server, via sha1 hash
def file_already_on_server(server_url, api_token, bytes):
	sha1 = hashlib.sha1(bytes).hexdigest()
	url = server_url + '/api/v1/document-sets/files/' + sha1
	r = requests.head(url, auth=(api_token,'x-auth-token'))

	return r.status_code == 204  # 204 = already got it, 404 = don't got it


# per http://docs.overviewproject.apiary.io/#reference/files/file/upload-file?console=1
def upload_single_file(server_url, api_token, filename, skip_existing=False):
	global files_uploaded

	if not file_readable_by_overview(filename):
		print("Skipping " + filename + ", Overview cannot read this format")
		return

	bytes = open(filename, 'rb').read()

	if skip_existing and file_already_on_server(server_url, api_token, bytes):
		print("Skipping " + filename + ", already on server")
		return
	else:
		print("Uploading " + filename + "...")

	url = server_url + '/api/v1/files/' + str(uuid.uuid4())
	headers = { 'content-disposition' : rfc6266.build_header(filename),
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

def upload_directory(server_url, api_token, filename, skip_existing=False):
	for subdir, dirs, files in os.walk(filename):
	    for file in files:

	    	if file[0]=='.':
	    		continue		# don't upload normally hidden files (I'm looking at you, .DS_store)

	    	fullname = os.path.join(subdir, file)
	    	try:
	    		upload_single_file(server_url, api_token, fullname, skip_existing=skip_existing)
	    	except Exception as e:
	    		print("Error, skipping " + fullname)
	    		traceback.print_exc()
	    		print('')

# ---- Main ----

parser = argparse.ArgumentParser(description='Upload a file or directory to an Overview server.')
parser.add_argument('file', help='file or directory to upload')
parser.add_argument('-t', '--token', help='API token corresponding to document set', required=True)
parser.add_argument('-s', '--server', help='url of Overview server, defaults to http://localhost:9000', default='http://localhost:9000')
parser.add_argument('-n', '--noskip', help='Don\'t skip files already on server', action="store_true")
args = parser.parse_args()

skip_existing = not args.noskip

filename = args.file.rstrip('/')  # removing trailing slash important for consistent directory handling

if not os.path.exists(filename):
	print("Cannot find file or directory " + filename)
else:
	ispath = os.path.isdir(filename)

	# do this all from directory containing specified file, to get consistent file titles 
	# if user specified a file, the filename (no path) is a title
	# if user specified a directory, that directory name (no path) is the base of the title
	basename = os.path.basename(filename)	
	dirname = os.path.dirname(filename)
	if dirname!='':
		os.chdir(dirname)

	if ispath:
		upload_directory(args.server, args.token, basename, skip_existing=skip_existing)
	else:
		upload_single_file(args.server, args.token, basename, skip_existing=skip_existing)

	# Send a finish only if we actually uploaded something (may have skipped all)
	if files_uploaded > 0:
		finish_upload(args.server, args.token,)



