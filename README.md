cat /etc/hosts
...
172.17.0.21 node1.example.com
172.17.0.22 node2.example.com
172.17.0.23 node3.example.com
172.17.0.24 node4.example.com
...

cd swarm_matchbox
./scripts/get-coreos stable 1576.4.0 $PWD/config/assets

sudo ./scripts/devnet create swarm
sudo ./scripts/libvirt create


