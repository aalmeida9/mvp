#for application logic
import json
import requests

#for Flask
from flask import render_template, redirect, request
from frontend import app

#address to the blockchain we are interacting with
BC_ADDRESS = "http://127.0.0.1:8000"

#address to the ryu controller
RYU_ADDRESS = "http://0.0.0.0:8080"
#alternatively: "http://127.0.0.1:8080" "http://localhost:8080"

ruleList = []
#potentially create rule class based on  rule formats, rule_id
#{"nw_src": "10.0.0.1/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP"} pings
#rules are registered to the switch as flow entries

#make sure duplicate rules don't get added to firewall 
cRules = ()


#get firewall rules from BC
def get_rules():
    chain_address = "{}/chain".format(BC_ADDRESS)
    response = requests.get(chain_address)

    global ruleList
    ruleList = []
    if response.status_code == 200:
        #chain is a dict response.content is bytes
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for rule in block["transactions"]:
                #print(rule)
                ruleList.append(rule)
    else:
        print("Unable to access blockchain {}".format(response.status_code))

#configure SDN firewall with rules from BC, current method works
#still need to enable communication on Firewall:
#put http://localhost:8080/firewall/module/enable/0000000000000001
def post_rules():
    address = "{}/firewall/rules/0000000000000001".format(RYU_ADDRESS)
    rule = {"nw_src": "10.0.0.1/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP"}
    r = requests.post(address, data=rule)

    #make sure to remove timestamp before sending POST request
    #for rule in ruleList:


@app.route("/")
def index():
    get_rules()
    #index.html template needs to be configured to initially display rules
    return render_template('index.html', title="index",
    node_address = BC_ADDRESS, ryu_address = RYU_ADDRESS, rules = ruleList)

#route for adding rules from the form to the BC/Controller
#add logic to make rules go both ways possible an HTML button
#add logic to stop duplicate rules probably in node_server
@app.route("/add", methods=['POST'])
def add():
    ip_src = request.form["src"]
    ip_dst = request.form["dst"]
    type = request.form["dropdown"]
    action = request.form['action']

    rule = {
        'nw_src': ip_src,
        'nw_dst': ip_dst,
        'nw_proto': type,
        'action': action
    }

    # Submit a transaction to the blockchain
    new_tx_address = "{}/new_transaction".format(BC_ADDRESS)
    mine_address = "{}/mine".format(BC_ADDRESS)

    requests.post(new_tx_address, json=rule,
    headers={'Content-type': 'application/json'})

    #add rule to controller after validated on BC (test this)
    address = "{}/firewall/rules/0000000000000001".format(RYU_ADDRESS)
    requests.post(address, json=rule,
    headers={'Content-type': 'application/json'})

    return redirect('/')

#initial test for viewing chain
@app.route("/test")
def test():
    address = "{}/chain".format(BC_ADDRESS)
    r = requests.get(address)
    print(json.loads(r.content))

    return 'test'
