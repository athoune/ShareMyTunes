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
- opensearch
- bottle

Setup will fetch them.

::

  python setup.py build

Web UI use :

- jquery
- soundmanager2

Testing
=======

::

  sudo python ./setup.py install
  shareMyTunes-index
  shareMyTunesd

You can test it here : http://localhost:8000

Features
========

- √ Rich Web interface
- √ Play music in web
- _ Play complete album
- √ Display artwork
- √ Nice CD display with http://www.komodomedia.com/blog/2009/03/sexy-music-album-overlays/
- √ Search track, album and artist
- _ Group result by album
- _ Abstract music db parsing, not only iTunes XML
- _ Multiple server query, with bonjour
- _ Downlaod album as a ZIP
- _ Share ipod connected to the computer
- √ Opensearch