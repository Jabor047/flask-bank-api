FROM python:3.9.4

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip3 install -r ./api/requirements.txt
RUN python3 ./api/models/database.py
RUN python3 ./api/insert_db.py
ENV FLASK_APP=api
CMD ["flask", "run", "--host", "0.0.0.0"]
EXPOSE 5000