FROM python:3.11

COPY . /home/im_productive_bot

WORKDIR /home/im_productive_bot

RUN pip install -r requirements.txt

ENV PYTHONPATH="/home/im_productive_bot"

CMD python3 bin/main.py
