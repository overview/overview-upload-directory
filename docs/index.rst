.. overview-upload documentation master file, created by
   sphinx-quickstart on Thu Jun  8 11:50:45 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to overview-upload's documentation!
===========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Upload files and directories to Overview.

Installation
============

``sudo pip3 install overview-upload``

Example Usage
=============

.. code-block:: python

   import overview_upload

   server = 'https://www.overviewdocs.com'
   # Generate an API token by browsing to
   # https://www.overviewdocs.com/documentsets/[ID]/api-tokens
   # (where `[ID]` is an existing document-set ID.
   api_token = 'rakhtasd...'

   upload = overview_upload.Upload(server, api_token)

   # Want to see what's happening? This will print to stderr:
   import logging
   upload.logger.setLevel(logging.DEBUG)
   upload.logger.addHandler(logging.StreamHandler())

   # Delete server-side uploaded, un-processed files
   upload.clear_previous_upload()

   # Upload all files in this directry, with titles relative to
   # this directory
   upload.send_directory('.')

   # Upload a specific file
   import pathlib
   upload.send_path_if_conditions_met(
       pathlib.Path('index.md'), # valid Path
       'doc/index.md'            # Overview document title
   )

   # Upload a BytesIO object. This will read the whole file
   # into memory before uploading it.
   #
   # In this example, we'll upload Overview's own homepage.
   import urllib
   url = 'https://www.overviewdocs.com'
   overview_title = url + '/index.html'
   with urllib.request.urlopen(url) as r:
       upload.send_file_if_conditions_met(r, overview_title)

   # Finally, now that we've uploaded all these files, let's
   # add them to the document set! The API token specifies
   # which document set we'll add to.
   upload.finish(lang='en', ocr=False, split_by_page=False)

   # And then browse to
   # https://www.overviewdocs.com/documentsets/[id] -- there
   # will be new documents for the files you uploaded.

API
===

.. automodule:: overview_upload

.. autoclass:: Upload
   :members:
