#!/bin/sh
apt-get update
apt-get install -y git
git clone http://192.168.0.162:3002/edwardjgriggs/pizza-dough-calculator.git /app
pip install --no-cache-dir -r /app/requirements.txt
python /app/Dough_Calculator.py
