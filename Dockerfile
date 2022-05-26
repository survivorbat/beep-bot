FROM python:3.10

WORKDIR /app

RUN apt-get update -y \
 && apt-get install -y \
    fluidsynth \
    ffmpeg \
    libffi-dev \
    python3.10-dev \
    libsodium-dev \
    lsof

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-u" , "main.py"]
