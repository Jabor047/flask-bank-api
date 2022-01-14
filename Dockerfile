FROM python:3.9.4

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip3 install -r ./api/requirements.txt
ENV FLASK_APP=api
CMD ["flask", "run", "--host", "0.0.0.0"]
