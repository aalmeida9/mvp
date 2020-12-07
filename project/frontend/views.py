#for application logic
import requests
import json
from hashlib import sha256

#for Flask
from flask import render_template, redirect, request
from frontend import app

#address to the blockchain we are interacting with
BC_ADDRESS = "http://127.0.0.1:8000"

#address to the ryu controller
RYU_ADDRESS = "http://0.0.0.0:8080"
#alternatives "http://127.0.0.1:8080" "http://localhost:8080"

#rules on the firewall
ruleList = []
#hashes of acceptable rules (from BC)
hashList = []

#potentially create rule class based on  rule format
#{"nw_src": "10.0.0.1/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP"} pings
#rules are registered to the switch as flow entries

#make sure duplicate rules don't get added to firewall

#get firewall rules from BC, change to just hashes?
def get_rules():
    chain_address = "{}/chain".format(BC_ADDRESS)
    response = requests.get(chain_address)

    if response.status_code == 200:
        #chain is a dict response.content is bytes
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for rule in block["transactions"]:
                #inital logic for getting rule hashes on genesis block
                if block["index"] == 0:
                    hashList.append(rule)
                else:
                    if rule not in ruleList:
                        ruleList.append(rule)
    else:
        print("Unable to access blockchain {}".format(response.status_code))

#configure SDN firewall with rules from BC, current method works (not used)
#still need to enable communication manually on Firewall:
#put http://localhost:8080/firewall/module/enable/0000000000000001
def post_rules():
    address = "{}/firewall/rules/0000000000000001".format(RYU_ADDRESS)
    rule = {"nw_src": "10.0.0.1/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP"}
    r = requests.post(address, data=rule)


@app.route("/")
def index():
    get_rules()
    return render_template('index.html', title="index",
    node_address = BC_ADDRESS, ryu_address = RYU_ADDRESS, rules = ruleList)

#route for adding rules from the form to the BC/Controller
@app.route("/add", methods=['POST'])
def add():
    #Load neccessary attributes for firewall rule from HTML form
    ip_src = request.form["src"]
    ip_dst = request.form["dst"]
    proto_type = request.form["dropdown"]
    action = request.form['actions']

    #add logic to make rules go both ways possibly an HTML button

    #create a dictionary to represent the firewall rule
    rule = {
        'nw_src': ip_src,
        'nw_dst': ip_dst,
        'nw_proto': proto_type,
        'actions': action
    }

    #add logic to stop duplicate rules

    #authenticate firewall rules for allowing traffic with hashes from BC
    if rule['actions'] == 'ALLOW':
        #returns a String
        ruleString = json.dumps(rule)
        #creates a hash
        ruleHash = sha256(ruleString.encode()).hexdigest()
        for hashes in hashList:
            if hashes == ruleHash:
                print("Hash matched: {}".format(hashes))
                print("Rule Authenticated: {}".format(rule))
                #add a redirect to double check a rule as is?
                if rule not in ruleList:
                    ruleList.append(rule)
                #break
    else:
        # Submit a transaction to the blockchain, only for DENY rules
        new_tx_address = "{}/new_transaction".format(BC_ADDRESS)
        mine_address = "{}/mine".format(BC_ADDRESS)

        requests.post(new_tx_address, json=rule,
        headers={'Content-type': 'application/json'})

    #add rule to rest_firewall (validate allow actions with BC) (test this)
    address = "{}/firewall/rules/0000000000000001".format(RYU_ADDRESS)
    requests.post(address, json=rule,
    headers={'Content-type': 'application/json'})

    return redirect('/')

#initial test for viewing chain
@app.route("/test")
def test():
    address = "{}/chain".format(BC_ADDRESS)
    r = requests.get(address)
    #print(json.loads(r.content))

    return 'test'
