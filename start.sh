#!/bin/bash
# Graph Editor Application start script
 
# Created: May 2017
# Author: nicolay-ryzhikov
 
echo GraphEditor Application started
 
python3 -m venv graphedit_venv
source graphedit_venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 main.py 