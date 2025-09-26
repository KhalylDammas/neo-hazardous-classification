# ####### 👇 SIMPLE SOLUTION (x86 and M1) 👇 ########
FROM python:3.10-slim

WORKDIR /prod

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y curl unzip && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY .env .env
COPY neo neo

RUN mkdir -p neo/raw_data

RUN curl -L -o neo/raw_data/nasa-nearest-earth-objects-1910-2024.zip\
    https://www.kaggle.com/api/v1/datasets/download/ivansher/nasa-nearest-earth-objects-1910-2024

RUN unzip neo/raw_data/nasa-nearest-earth-objects-1910-2024.zip -d neo/raw_data/
RUN rm neo/raw_data/nasa-nearest-earth-objects-1910-2024.zip

EXPOSE 8000 8501

CMD ["sh", "-c", "uvicorn neo.api.fast_api:app --host 0.0.0.0 --port $PORT & streamlit run neo/app/app_interface.py --server.port 8503 --server.address 0.0.0.0"]
