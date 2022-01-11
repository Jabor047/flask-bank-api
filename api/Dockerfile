FROM python:3.9.4

RUN mkdir /api
COPY . /api
WORKDIR /api

RUN pip3 install -r requirements.txt
RUN python3 /api/models/database.py
RUN python3 /api/insert_db.py
RUN export FLASK_APP=api
CMD ["flask", "run"]

EXPOSE 5000