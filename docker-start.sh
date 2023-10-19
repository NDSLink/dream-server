#!/bin/sh
flask db upgrade
python3 -m gunicorn -w 4 app:app -b 0.0.0.0:80