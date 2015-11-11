#!/bin/sh
killall python
python manage.py  runserver test.pychat.xyz:8000 &
#python manage.py  runserver 192.168.17.134:80 &
