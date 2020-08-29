FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

# Install dependencies...
#RUN pip install --upgrade pip
ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/