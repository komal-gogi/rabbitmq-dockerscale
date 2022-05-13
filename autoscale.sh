#!/bin/bash
  

# Build the docker image.
docker-compose build
echo -e '\n\n'
sleep 5s

# Initializing Docker swarm.
docker swarm leave --force
docker swarm init
echo -e '\n\n'

# We can join manager node to worker using "docker swarm join --token ip" command.

# Deploying docker swarm for single node using docker-compose.yml file.
docker stack deploy -c docker-compose.yml container
echo -e "\nservices created .........\n\n"
sleep 10s

# List the docker services and check for the created container
docker service ls
echo -e '\n\n'

#Connect to rabbitmq. If the messages in the queue is equal or greater then a certain threshold value,
#Docker swarm will scale up the containers else scale down.

sleep 8s
queue_msg=$(curl -s -u rabbituser:rabbitpass -H "content-type:application/json" \
-XGET -d'{"durable":true}' \
http://devrabbit.centralus.cloudapp.azure.com:15672/api/queues/scaletest/docker-scale | grep -o '"messages":[0-9]*' | awk -F ':' '{print $2}')


if [ $queue_msg -ge 50 ]
then 
    #Scale UP
    echo -e "scaling up the containers"
    docker service scale container_consumer=4
else
    #Scale DOWN
    echo -e "scaling down the containers"
    docker service scale container_consumer=3
fi

echo -e '\n\n'
sleep 10s
docker service ls
