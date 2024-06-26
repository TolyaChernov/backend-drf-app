FROM python:3.12-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip

RUN pip install drf-spectacular

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000


# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]