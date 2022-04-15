
FROM python:3.9-alpine

WORKDIR /app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk update

# install dependencies
COPY req_3_9.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip &&\
 pip install --no-cache-dir -r requirements.txt &&\
 pip install --no-cache-dir gunicorn==20.1.0


COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]
