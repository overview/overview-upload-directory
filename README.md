# overview-upload-directory
A script to upload / sync a directory of document files to an Overview server

# usage
`python upload.py -t <API_TOKEN> -s <SERVER_URL> [-n] file`

* `API_TOKEN` is the access token for a particular document set, which you get like this

   1. Browse to your document set. The URL will look like `https://www.overviewdocs.com/documentsets/123456`.
   2. Note the document set number, in this case 123456
   3. Browse to `https://www.overviewdocs.com/documentsets/[your number here]/api-tokens` and click "Generate token".

* `SERVER_NAME` is the base URL for the server, which defaults to http://localhost:9000 for use with overview-local

* `-n` means don't skip already uploaded files, if specified

* `file` is the name of a file, or a directory. 

Note that the document tiles in Overview will have any preceding path stripped off. So `upload some/path/to/directory` will produce titles of the form `directory/file1`, `directory/subdir/file2`, etc. If you want to preserve `some/path/to`, do `upload some`

Requires python3

