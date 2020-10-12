FROM python:latest
WORKDIR /usr/src
ADD /app /usr/src
RUN pip install -r requirements.txt
EXPOSE 5000