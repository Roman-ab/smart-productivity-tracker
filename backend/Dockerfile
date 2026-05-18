FROM python:3.14.5-slim

WORKDIR /app

COPY . . 

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python" "main.py"]
