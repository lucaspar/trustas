#!/bin/bash

# Environment variables
export DYNAMIX_DIR=$HOME/dynam-ix-beta
export COMPOSE_PROJECT_NAME="net"

# Exit in case of errors
set -e

# Cleaning any previous experiment
echo "Cleaning docker environment"
docker rm -f $(docker ps -aq)
docker rmi $(docker images dev-* -q)
docker network prune -f
docker-compose -f docker-compose-base.yml down

# Start Docker Containers
echo "Staring docker containers"
docker-compose -f docker-compose-base.yml up -d orderer