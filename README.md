


#active venv
source venv/bin/activate


#Installation von redis-commander
sudo apt install npm
sudo npm install -g redis-commander

#Starte redis-commander:
redis-commander

#start the gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 your_app_module:app
gunicorn -w 4 -b 0.0.0.0:8000 app:app

#start gunicorn asyncrone
gunicorn -w 4 -b 0.0.0.0:8000 -k gevent app:app

#configure swagger UI
http://localhost:5000/api/docs/
or
http://0.0.0.0:8000/api/docs/#/

