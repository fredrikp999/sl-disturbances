#FROM python:3.4-alpine
FROM python:3.7.2-alpine3.8
ADD . /code
WORKDIR /code
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python", "app.py"]