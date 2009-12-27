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

Testing
=======

::

  cd src/shareMyTunes
  python server.py

You can test it here : http://localhost:8000

To do
=====

- Abstract music db parsing, not only iTunes XML
- Search track, album and artist
- Multiple server query, with bonjour