# 
FROM python:3.12-alpine

# 
WORKDIR /pet-name-game

# 
COPY /requirements.txt .

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
COPY app .

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]