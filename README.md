# Autoradar by Igor Morozov 
# GPS/Glonass monitoring server with tk103 gate
Autoradar server

A receiver and web-ui for data from Android based GPS trackers.
Build

git clone git@github.com:gadson/Autoradar
cd /GeoServer
edit file settings.py

EMAIL_HOST = 'smtp.yandex.ru' - smtp send mail server name
EMAIL_HOST_USER = 'info@*****.ru' smtp username
EMAIL_HOST_PASSWORD = '' smtp password
EMAIL_PORT = 587 smtp server port
EMAIL_USE_TLS = True
FROM_EMAIL='' from e-mail

#Main domain
MAIN_DOMAIN ='http://*******.com' 

#Google GCM PUSH service API key 
GOOGLE_API_KEY = "" 

#RocketChat server settings for log messages
RC_USERNAME = 'Robot_Vasia'
RC_PASSWORD = ''
RC_DOMAIN = 'http://*******:3000'



