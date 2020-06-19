FROM jenkins/jenkins:2.222.4-lts-alpine

USER root

RUN apk add --update docker openrc
RUN rc-update add docker boot

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN \
  ATTEMPTS=2 \
  /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt

# TODO: Check how to use Jenkins user UID=1000 and docker -> error when trying to access /var/run/docker.sock

# RUN addgroup jenkins docker

# USER 1000