FROM python:3.8-alpine

WORKDIR /app

RUN apk add --update \
    fluidsynth \
    ffmpeg

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "main.py"]
