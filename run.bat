@echo off
pip install -r requirements.txt
cd apis
python -m uvicorn main:app