FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .


RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn" , "main.app" , "--host" , "5637" , "--port" , "8000"]
