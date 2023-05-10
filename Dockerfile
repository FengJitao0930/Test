FROM python:3.9
LABEL authors="Eighteen"

COPY . .

RUN pip install couchdb;\
    pip install flask;\
    pip install flask-restful;\
    pip install flask_script;\
    pip install flask_migrate;\
    pip install flask-cors \

EXPOSE 8080

CMD["python", "app.py"]