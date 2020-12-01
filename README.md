# Zero Trust Architecture with Blockchain virtual lab

## Project setup

Ubuntu 18.04 is currently used for the development environment

```sh
# clone and enter repository
$ git clone https://github.com/aalmeida9/mvp.git
$ cd mvp
# setup and enter python virtual environment (optional)
$ python3 -m venv venv
$ source venv/bin/activate
# install required python packages
$ pip install -e .
# Or: pip install -r requirements.txt
```

## Flask Applications

The frontend web server and Blockchain application use the Flask microframework. The implementation of Blockchain is based on this repository: https://github.com/satwikkansal/python_blockchain_app/tree/ibm_blockchain_post

Each of the following blocks of commands need to be run in different terminals in order for the project to work properly.

### Blockchain startup

```sh
$ export FLASK_APP=node_server.py
$ export FLASK_ENV=development
$ flask run --port 8000
```

### Frontend Web server

```sh
$ python run.py
```

## Network Emulation

Network emulation uses Mininet. More information can be found here: http://mininet.org/

```sh
$ sudo mn --topo single,3 --mac --switch ovsk --controller remote
```

## Software Defined Networking (SDN) Controller

SDN controller use the Ryu framework for the firewall application. More information can be found here: https://ryu-sdn.org/

```sh
$ ryu-manager ryu.app.rest_firewall
```
