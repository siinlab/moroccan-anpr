FROM python:3.11.6

WORKDIR /root

COPY requirements.txt /root/
COPY src/ /root/src
COPY models/ /root/models
COPY scripts/ /root/scripts

RUN bash scripts/install.sh

ENTRYPOINT ["bash", "scripts/run.sh"]
