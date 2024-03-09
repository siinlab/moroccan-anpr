FROM python:3.11.6

WORKDIR /root

COPY requirements.txt /root/
COPY utils/ /root/utils
COPY src/ /root/src
COPY models/ /root/models
COPY scripts/ /root/scripts
COPY Documentation.md /root/Documentation.md
COPY CHANGELOG.md /root/CHANGELOG.md
COPY VERSION /root/VERSION

RUN bash scripts/install.sh

ENTRYPOINT ["bash", "scripts/run.sh"]
