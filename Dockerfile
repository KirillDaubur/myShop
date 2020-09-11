FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY van_oak/requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/