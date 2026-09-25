FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive TZ=UTC PYTHONUNBUFFERED=1 BRAIN_ENV=production PATH="/opt/venv/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl tzdata build-essential cmake git wget unzip pkg-config ffmpeg libglib2.0-0 libssl-dev libffi-dev python3.11 python3.11-venv python3-pip && rm -rf /var/lib/apt/lists/* && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

WORKDIR /app
COPY . /app
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --upgrade pip setuptools wheel && if [ -f /app/requirements.txt ]; then /opt/venv/bin/pip install -r /app/requirements.txt; fi
RUN mkdir -p /app/logs
EXPOSE 8080
CMD ["bash", "-lc", "if [ -f ./main.py ]; then python main.py; elif [ -f ./Brain/neomind/main.py ]; then python ./Brain/neomind/main.py; else python -m unittest discover -s tests -v; fi"]
