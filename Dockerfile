FROM python:3.8
WORKDIR /code
COPY . /code
RUN pip install -r /code/requirements.txt
EXPOSE 8000