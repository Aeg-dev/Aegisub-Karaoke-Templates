@echo off
TITLE ASS FX Viewer - log output
START "" /B  python-3.9.2-embed-win32\python.exe -m http.server 2333 --bind 127.0.0.1 --directory html
ECHO WEB Server ON
ECHO Opening webpage...
START ""  "http://localhost:2333"
@echo on
