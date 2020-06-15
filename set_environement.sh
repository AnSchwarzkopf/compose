#!/bin/sh

export DOCKER_HOST=$(hostname)

envsubst < 'prometheus/template_prometheus.yml' > 'prometheus/prometheus.yml'