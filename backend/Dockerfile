FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask flask-cors requests apscheduler

CMD ["python", "app.py"]