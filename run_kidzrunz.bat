@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Checking for outdated dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Applying migrations...
python manage.py makemigrations
python manage.py migrate

echo Collecting static files...
python manage.py collectstatic --noinput

echo Starting Django development server...
python manage.py runserver