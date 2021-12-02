FROM python:3.7.3
RUN mkdir /code
WORKDIR /code
ADD . /code/

## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

RUN pip install -r requirements.txt
CMD /wait && python app.py
