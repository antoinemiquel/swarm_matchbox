# project from "https://github.com/coreos/matchbox" to test a Docker swarm cluster

## Set /etc/hosts
cat /etc/hosts
...
172.17.0.21 node1.example.com
172.17.0.22 node2.example.com
172.17.0.23 node3.example.com
172.17.0.24 node4.example.com
...

## Add your id_rsa.pub 
Files : config/groups/swarm/*.json 
Section "ssh_authorized_keys"

## Download coreos image
cd swarm_matchbox
./scripts/get-coreos stable 1576.4.0 $PWD/config/assets

## Configure Docker daemon for local registry
Create or modify /etc/docker/daemon.json
{ "insecure-registries":["172.17.0.1:5000"] }
sudo systemctl restart docker.service

## Launch boot infrastructure
sudo ./scripts/devnet create swarm

## Launch virtual-machines
sudo ./scripts/libvirt create

## Run a local Docker registry
mkdir $PWD/registry/registry
docker run -d -p 5000:5000 --restart=always --name registry -v $PWD/registry/registry:/var/lib/registry registry:2

## Build nginx_test Docker image :
docker build -t 172.17.0.1:5000/nginx_test nginx_test
docker push 172.17.0.1:5000/nginx_test
docker image remove 172.17.0.1:5000/nginx_test

## Run a test swarm service
ssh core@node1.example.com
    docker service create --name my_web \
                          --replicas 3 \
                          --publish published=7000,target=80 \
                          172.17.0.1:5000/nginx_test

## Configure an external load balancer
docker run -d --name external_load_balancer -p 80:80 -v $PWD/haproxy:/usr/local/etc/haproxy:ro haproxy:1.8 

