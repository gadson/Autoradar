FROM python:3
RUN mkdir /data
WORKDIR /data
ADD . /data
ADD requirements.txt /data
RUN pip install -r requirements.txt
CMD python ./manage.py runserver --insecure 0.0.0.0:8001
