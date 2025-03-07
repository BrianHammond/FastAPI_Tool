FROM python:3.13.2-alpine3.21

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "application:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
