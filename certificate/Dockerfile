FROM python:3.8-slim

COPY requirements.txt requirements.txt

RUN apt-get update \
    && pip3 install -r requirements.txt

COPY checkAndRenewCertificates.py /home/script/checkAndRenewCertificates.py
CMD ["python3", "-u", "/home/script/checkAndRenewCertificates.py"]