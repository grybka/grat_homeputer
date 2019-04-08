# grat_homeputer
So this really ought to be done in docker-compose, but given it won't install on my raspberry pi, here are the commands to start stuff

#create the container that works locally on a pi
docker build -t local_dragonfly .

#rabbitmq broker
docker run --rm -d -p 5672:5672 rabbitmq:3-management-alpine

#a thing that sets up the exchange
docker run --rm -v ./local_dragonfly/project8_authentications.json:/root/.project8_authentications.json local_dragonfly dragonfly monitor -vv -b rabbit_broker -e alerts
