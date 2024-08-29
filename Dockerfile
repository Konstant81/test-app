FROM python:3.11.2

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]