Share My Tunes
==============

Play and search distant iTunes with web.

Building
========

Dependencies are :

- genshi
- whoosh
- mutagen
- pybonjour

Setup will fetch them.

::

  python setup.py build

Web UI use :

- jquery
- soundmanager2

Testing
=======

::

  cd src/shareMyTunes
  python server.py

You can test it here : http://localhost:8000

Features
========

- x Rich Web interface
- x Play music in web
- _ Play complete album
- x Display artwork
- x Search track, album and artist
- _ Group result by album
- _ Abstract music db parsing, not only iTunes XML
- _ Multiple server query, with bonjour
- _ Downlaod album as a ZIP