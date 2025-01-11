#!/bin/bash
source /home/portpass/cctv_app/venv/bin/activate
export FLASK_APP=/home/portpass/cctv_app/main.py
flask run -h 0.0.0.0  --cert=cert.pem --key=priv_key.pem
