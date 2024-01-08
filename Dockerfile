# syntax=docker/dockerfile:1

# Hosting docker on render.com requires linux/amd64
# https://docs.render.com/deploy-an-image#image-requirements
FROM --platform=linux/amd64 python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
CMD ["python", "main.py"]
