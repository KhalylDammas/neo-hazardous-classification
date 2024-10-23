# ####### 👇 SIMPLE SOLUTION (x86 and M1) 👇 ########
FROM python:3.10.6-buster

WORKDIR /prod

COPY requirements_prod.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY neo neo
COPY raw_data raw_data

CMD uvicorn neo.api.fast_api:app --host 0.0.0.0 --port $PORT
