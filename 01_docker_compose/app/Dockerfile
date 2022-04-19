
FROM python:3.9-alpine

WORKDIR /app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update &&\
    apk --no-cache add gettext

# install dependencies
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip &&\
 pip install --no-cache-dir -r requirements.txt &&\
 pip install --no-cache-dir gunicorn==20.1.0


COPY . .

RUN python manage.py collectstatic &&\
    python manage.py compilemessages

RUN sed -i 's/\r$//g' /app/entrypoint.sh &&\
    chmod +x /app/entrypoint.sh


CMD ["/app/entrypoint.sh", "gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]
