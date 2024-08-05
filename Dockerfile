FROM python:3.12-alpine3.19

WORKDIR /telegram-bot

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]