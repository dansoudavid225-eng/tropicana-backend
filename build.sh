#!/usr/bin/env bash
set -e
pip install -r requirements.txt
python fix_db.py
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py reset_admin
