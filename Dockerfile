FROM selenium/standalone-chrome:127.0

USER root

RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y ffmpeg python3-pip python3.12  python3.12-venv  \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .

COPY youtube_auto_publish ./youtube_auto_publish

COPY test.py .

RUN python3.12 -m venv /app/venv && \
    /app/venv/bin/pip install -r requirements.txt

CMD ["sh", "-c",". /app/venv/bin/activate && python test.py"]