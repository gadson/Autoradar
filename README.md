# Autoradar by Igor Morozov 
# GPS/Glonass monitoring server with tk103 gate
Autoradar server

A receiver and web-ui for data from Android based GPS trackers.
Build

git clone git@github.com:gadson/Autoradar<br>
cd /GeoServer<br>
edit file settings.py<br>

EMAIL_HOST = 'smtp.yandex.ru' - smtp send mail server name<br>
EMAIL_HOST_USER = 'info@*****.ru' smtp username<br>
EMAIL_HOST_PASSWORD = '' smtp password<br>
EMAIL_PORT = 587 smtp server port<br>
EMAIL_USE_TLS = True<br>
FROM_EMAIL='' from e-mail<br>

#Main domain<br>
MAIN_DOMAIN ='http://*******.com' <br>
<br>
#Google GCM PUSH service API key <br>
GOOGLE_API_KEY = "" <br>
<br>
Chat server settings for log messages<br>
RC_USERNAME = 'Robot_Vasia'<br>
RC_PASSWORD = ''<br>
RC_DOMAIN = 'http://*******:3000'<br>



