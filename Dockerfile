FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/

RUN chmod +x entry.sh

CMD ["./entry.sh"]
