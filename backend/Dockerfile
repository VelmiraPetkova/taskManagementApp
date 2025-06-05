FROM python:3.10-slim

WORKDIR /app

COPY ./backend ./backend
COPY *.py .
COPY requirements.txt .

ENV FLASK_APP=/app/main.py

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "main.py"]
