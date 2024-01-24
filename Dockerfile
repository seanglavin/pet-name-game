# 
FROM python:3.12-alpine

# 
WORKDIR /pet-name-game

# 
COPY ./requirements.txt /pet-name-game/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /pet-name-game/requirements.txt

# 
COPY ./app /pet-name-game/app

# 
CMD ["uvicorn", "app.main:app", "--reload"]