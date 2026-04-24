#!/usr/bin/env bash
pip install -r requirements.txt
cd anj_lapastora 
python manage.py collectstatic --noinput
python manage.py migrate

&& pip install -r requirements.txt