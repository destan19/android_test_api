#!/bin/sh
killall python
python manage.py  runserver 192.168.17.134:80 &
#python manage.py  runserver 192.168.17.134:80 &
