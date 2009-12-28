#!/bin/sh

cd $(dirname "$0")
python -c 'from shareMyTunes.server import local
local()'
