FROM python:3.12-slim

WORKDIR /app

COPY . . 

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn" , "main.app" , "--host" , "5637" , "--port" , "8000"]
