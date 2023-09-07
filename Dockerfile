FROM python:3.9-slim-bookworm
EXPOSE 8000
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

RUN python ./predownload.py

CMD ["python3", "-m", "gunicorn", "-w", "4", "main:app"]