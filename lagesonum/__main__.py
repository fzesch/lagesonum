# coding: utf-8

# Datei zum lokalen testen, PythonAnywhere verwendet bottle_app.py direkt

from bottle import run, debug

from bottle_app import application

debug(True)
run(application, host='localhost', port=8080, reloader=True)
