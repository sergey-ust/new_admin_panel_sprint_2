
FROM python:3.9-alpine

WORKDIR /app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update &&\
    apk --no-cache add gettext


COPY . .

# install dependencies
RUN pip install --no-cache-dir --upgrade pip &&\
 pip install --no-cache-dir -r requirements.txt &&\
 pip install --no-cache-dir gunicorn==20.1.0


# prepare app data
RUN python manage.py collectstatic --clear --noinput &&\
    python manage.py compilemessages

# create entrypoint for DB waiting
RUN sed -i 's/\r$//g' /app/entrypoint.sh &&\
    chmod +x /app/entrypoint.sh


CMD ["/app/entrypoint.sh", "gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]
