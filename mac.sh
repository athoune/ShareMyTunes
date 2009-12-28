#!/bin/sh

mkdir -p dist/demo
cp -rv /Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/whoosh dist/demo/
cp -rv /Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/genshi dist/demo/
cp -rv /Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/mutagen dist/demo/
cp -rv /Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/pybonjour.py dist/demo/

python setup.py build
cp -rv build/lib/shareMyTunes dist/demo/
cp -rv src/shareMyTunes/data dist/demo/shareMyTunes/
find dist/demo -name "*.pyc" -exec rm {} \;
find dist/demo -name ".DS_Store" -exec rm {} \;
cp -av shareMyTunes.command dist/demo/

