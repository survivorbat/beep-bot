FROM python:3.8-alpine

WORKDIR /app

RUN apk add --no-cache --virtual --update \
    fluidsynth \
    ffmpeg \
    build-base \
    libffi-dev \
    libsodium \
    make \
    cmake \
    .pynacl_deps \
    python3-dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-u" , "main.py"]
