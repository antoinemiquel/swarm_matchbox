# Test the deployment of a docker swarm on coreos
## project inspiration : [CoreOs Matchbox](https://github.com/coreos/matchbox)
___

## Set /etc/hosts
Add adresses of kvm machines in `/etc/hosts` of your local machine
```{r, engine='bash'}
cat /etc/hosts
...
172.17.0.21 node1.example.com
172.17.0.22 node2.example.com
172.17.0.23 node3.example.com
172.17.0.24 node4.example.com
...
```

## Add your id_rsa.pub
In order to connect to the VMs, it is necessary to set a ssh public key in files : `config/groups/swarm/*.json` s(ection "ssh_authorized_keys")

___

## Download coreos image
```{r, engine='bash'}
cd swarm_matchbox
./scripts/get-coreos stable 1576.4.0 $PWD/config/assets
```

## Configure Docker daemon for local registry
Create or modify `/etc/docker/daemon.json`
{ "insecure-registries":["172.17.0.1:5000"] }

Restart Docker daemon to take into account
```{r, engine='bash'}
sudo systemctl restart docker.service
```

## Launch boot infrastructure
```{r, engine='bash'}
sudo ./scripts/devnet create swarm
```

## Launch virtual-machines
```{r, engine='bash'}
sudo ./scripts/libvirt create
```
___

## Run a local Docker registry/registry
```{r, engine='bash'}
mkdir $PWD/registry/registry
docker run -d -p 5000:5000 --restart=always --name registry -v $PWD/registry/registry:/var/lib/registry registry:2
```

## Build web_test (python web page) Docker image :
```{r, engine='bash'}
docker build -t 172.17.0.1:5000/web_test web_test
docker push 172.17.0.1:5000/web_test
docker image remove 172.17.0.1:5000/web_test
```

## Run a test swarm service
```{r, engine='bash'}
ssh core@node1.example.com
    docker service create --name my_web \
                          --replicas 3 \
                          --publish published=7000,target=8080 \
                          172.17.0.1:5000/web_test
```

## Configure an external load balancer
```{r, engine='bash'}
docker run -d --name external_load_balancer -p 80:80 -v $PWD/haproxy:/usr/local/etc/haproxy:ro haproxy:1.8
```
