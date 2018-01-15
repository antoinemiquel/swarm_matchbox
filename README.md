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

## Configure an external load balancer
docker run -d --name external_load_balancer -v $PWD/haproxy:/usr/local/etc/haproxy:ro haproxy:1.8 

## Run a test swarm service
ssh core@node1.example.com
    docker service create --name my_web nginx
    docker service update --publish-add 80 my_web
