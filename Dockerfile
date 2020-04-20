FROM python:3

WORKDIR /usr/src/app

RUN pip3 install pandas
RUN pip3 install psycopg2
RUN pip install lxml
RUN pip install matplotlib

COPY . .

CMD [ "echo", "INICIANDO" ]