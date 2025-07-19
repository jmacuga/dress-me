FROM python:3.9-slim

WORKDIR /app

# commons
RUN apt-get update
RUN apt-get install -y \ 
        gcc \
        libffi-dev \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*

COPY pre-requirements.txt .
RUN pip install --upgrade pip && pip install  --no-cache-dir -r pre-requirements.txt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--debug"]
