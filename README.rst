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

- ☑ Rich Web interface
- ☑ Play music in web
- ☐ Play complete album
- ☑ Display artwork
- ☑ Search track, album and artist
- ☐ Group result by album
- ☐ Abstract music db parsing, not only iTunes XML
- ☐ Multiple server query, with bonjour
- ☐ Downlaod album as a ZIP