# Autoradar GPS/GLONASS service
GPS/Glonass monitoring server an open source GPS/GLONASS tracking system. This repository contains Python back-end service. It support tk102-103 protokol. It also provides easy to use REST API.

Other parts of Autoradar GPS/GLONASS service solution include:

    Autoradar web app
    Autoradar Manager Android app
    Autoradar Manager iOS app

installation:<br>

cd /GeoServer<br>
insall in docker postgress<br>
edit file settings.py<br>
Configure bd<br>
        'NAME': 'postgres',<br>
        'USER': 'postgres',<br>
        'PASSWORD': 'postgres',<br>
        'HOST': 'db',<br>
        'PORT': '5432',<br>
    
Configure other settings<br>
EMAIL_HOST = 'smtp.yandex.ru' - smtp send mail server name<br>
EMAIL_HOST_USER = 'info@*****.ru' smtp username<br>
EMAIL_HOST_PASSWORD = '' smtp password<br>
EMAIL_PORT = 587 smtp server port<br>
EMAIL_USE_TLS = True<br>
FROM_EMAIL='' from e-mail<br>

#Main domain<br>
MAIN_DOMAIN ='http://mysite.com' <br>
<br>
Google GCM PUSH service API key <br>
GOOGLE_API_KEY = "" <br>
<br>
Chat server settings for log messages<br>
RC_USERNAME = 'Robot_Vasia'<br>
RC_PASSWORD = ''<br>
RC_DOMAIN = 'http://mychatserver.com:3000'<br>

cd ..

sudo docker build -t geoserver .<br>
sudo docker run --restart=always -d -p 8001:8001 geoserver<br>
docker-compose run geoserver python manage.py migrate<br>
docker-compose run geoserver python manage.py createsuperuser<br>


