overview-upload
===============

Upload files to an `Overview <https://www.overviewdocs.com>`__ document
set.

Installation
============

Requires `python3 <https://www.python.org/>`__.

``pip3 install overview_upload``, maybe with ``sudo`` in front. That
will install a ``overview-upload`` program in your path.

Command-Line Usage
==================

overview-upload: upload files
-----------------------------

``overview-upload --server <SERVER_URL> --token <API_TOKEN> [options] DIRECTORY``

Required arguments:

-  ``SERVER_URL`` is the base URL for the server, which defaults to
   http://localhost:9000 for use with
   `overview-local <https://github.com/overview/overview-local>`__.
-  ``API_TOKEN`` is the access token for a particular document set,
   which you get like this:

   1. Browse to your document set. The URL will look like
      ``https://www.overviewdocs.com/documentsets/123456``.
   2. Note the document set number, in this case ``123456``
   3. Browse to
      ``https://www.overviewdocs.com/documentsets/[your number here]/api-tokens``
      and click "Generate token".

-  ``DIRECTORY`` is a path to the file or directory you want to upload.

Optional arguments:

-  ``--skip-duplicate`` (the default), ``--noskip``: skip files that are
   already part of the document set your API token refers to. Files are
   compared by their sha1 hashes, meaning even if you move or rename the
   file it will not be uploaded if the document set already includes it.
   This feature is helpful for synchronizing a local directory with an
   Overview document set; however, it will not delete Overview documents
   corresponding to files you deleted locally.
-  ``--split-by-page``: tell Overview to turn a multi-page file (like a
   PDF or Word document) into several Overview documents.
-  ``--ocr`` (the default), ``--no-ocr``: tell Overview what to do when
   a PDF page has only images but no text. Overview can either try to
   recognize text using
   `Tesseract <https://github.com/tesseract-ocr/tesseract>`__ (which is
   slow and will prevent you from viewing the document set until it
   finishes), or it can assume the page contains no text.
-- ``create-document-set-with-title``: create a new document set with the
   given title and then add files to it. ``API_TOKEN`` here is one you
   create at http://www.overviewdocs.com/api-tokens or
   http://localhost:9000/api-tokens.

If you upload a single file, its Overview document title will be its
filename, without any directory information. If you upload a directory,
filenames will include subdirectory informatin: for instance, if
``overview-upload /some/path`` uploads ``/some/path/to/file.pdf``, the
Overview document title will be ``to/file.pdf``.

overview-upload-csv: upload from a CSV manifest
-----------------------------------------------

Given a CSV like this:

.. csv-table:: manifest.csv
   :header: id,title,url,field1,field2
   
   1,doc1.pdf,http://www.adobe.com/content/dam/Adobe/en/devnet/acrobat/pdfs/pdf_open_parameters.pdf,some metadata,some more metadata
   2,doc2.pdf,http://www.adobe.com/content/dam/Adobe/en/devnet/acrobat/pdfs/pdf_open_parameters.pdf,more metadata,and even more metadata

You can upload the referenced files to Overview like this:

``overview-upload-csv <API_TOKEN> <manifest.csv> --url-field url --title-field title --server https://www.overviewdocs.com``

If you browse to the document set and add ``field1`` and ``field2`` fields, you
will see the values from the CSV.

You can use ``--local-file-field`` instead of ``--url-field`` to use a field containing paths on your filesystem.

overview-create-document-set: Create an empty document set
----------------------------------------------------------------

You can create an empty document set using this incantation:

``overview-create-document-set --server <SERVER_URL> --token <API_TOKEN> [options] "DOCUMENT SET TITLE"``

Required arguments:

-  ``SERVER_URL`` is the base URL for the server, which defaults to
   http://localhost:9000 for use with
   `overview-local <https://github.com/overview/overview-local>`__.
-  ``API_TOKEN`` is the *global* access token for creating document sets,
   which you can create at https://www.overviewdocs.com/api-tokens

Optional arguments:

- ``--metadata-schema-field-names``: Fields to display for each document. Example: ``"Title,Author"``.

The program will display an API token you can use to add documents to the new
document set.

API usage
=========

You can also ``import overview_upload`` from your own Python3 program
and then use the ``overview_upload.Upload`` class. See the
``overview-server`` source code for more information.

Developing
==========

Releasing a new version
-----------------------

0. `Register on
   PyPI <https://pypi.python.org/pypi?%3Aaction=register_form>`__ and
   create ``~/.pypirc`` with ``[pypi]\nusername = ...\npassword = ...``
1. Update ``version`` in ``setup.py``
2. ``rm -r dist && ./setup.py sdist``
3. ``gpg --detach-sign -a dist/*.tar.gz``
4. ``twine upload dist/*.tar.gz dist/*.asc``

License
=======

This software is distributed under the terms of the GNU Affero General
Public License. See the LICENSE file for details.
