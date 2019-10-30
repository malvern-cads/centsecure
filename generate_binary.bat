@echo off
echo Updating dependencies...
python -m pip install --upgrade pip
python -m pip install pipenv
python -m pipenv install --dev
echo Generating binary...
python -m pipenv run pyinstaller -y --add-data "payloads;payloads/." -F centsecure.py
echo Done. Look in the 'dist' folder