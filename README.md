# grat_homeputer
So this really ought to be done in docker-compose, but given it won't install on my raspberry pi, here are the commands to start stuff

#rabbitmq broker
docker run -p 5672:5672 rabbitmq:3-management 

#a thing that sets up the exchange
docker run -v "./local_dragonfly/project8_authentications.json":"/root/.project8_authentications.json" "dragonfly monitor -vv -b rabbit_broker -e alerts"
