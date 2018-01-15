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

## Launch boot infrastructure
sudo ./scripts/devnet create swarm

## Launch virtual-machines
sudo ./scripts/libvirt create

## Run a local Docker registry
docker run -d -p 5000:5000 --restart=always --name registry -v $PWD/registry:/var/lib/registry registry:2

### example 1 :
docker pull nginx:1.13
docker tag nginx:1.13 matchbox.example.com:5000/nginx
docker push matchbox.example.com:5000/nginx
docker image remove nginx:1.13
docker image remove matchbox.example.com:5000/nginx

### example 2 :
docker build -t nginx_test matchbox.example.com:5000/nginx_test
docker push matchbox.example.com:5000/nginx_test
docker image remove matchbox.example.com:5000/nginx_test

## Run a test swarm service
ssh core@node1.example.com
    docker service create --name my_web \
                          --replicas 3 \
                          --publish published=8080,target=80 \
                          matchbox.example.com:5000/nginx_test

## Configure an external load balancer
docker run -d --name external_load_balancer -v $PWD/haproxy:/usr/local/etc/haproxy:ro haproxy:1.8 
