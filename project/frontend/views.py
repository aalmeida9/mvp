#for application logic
import json
import requests

#for Flask
from flask import render_template, redirect, request
from frontend import app

#address to the blockchain node we are interacting with
BC_ADDRESS = "http://127.0.0.1:8000"

#address to the ryu controller
RYU_ADDRESS = "http://0.0.0.0:8080"
#alternatively: "http://127.0.0.1:8080" "http://localhost:8080"

#rules is a list of dictionaries
ruleList = []

#potentially create rule class based on  rule formats
#{"nw_src": "10.0.0.1/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP"} pings
#also rule_id
#rules are registered to the switch as flow entries

#get firewall rules from BC
#BC still needs to be configured before using this method!
def get_rules():
    chain_address = "{}/chain".format(BC_ADDRESS)
    response = requests.get(chain_address)
    if response.status_code == 200:
        chain = json.loads(response.content)
        #loads rules from chain into ruleList

#configure SDN firewall with rules from BC, current method works
#still need to enable communication on Firewall:
#put http://localhost:8080/firewall/module/enable/0000000000000001
def post_rules():
    address = "{}/firewall/rules/0000000000000001".format(RYU_ADDRESS)
    rule = {"nw_src": "10.0.0.1/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP"}
    r = requests.post(address, data=rule)

    return r


@app.route("/")
def index():
        #index.html template needs to be configured to initially display rules
        return render_template('index.html', title="index", rules = ruleList)

#initial test function for testing if firewall rules updated
@app.route("/test")
def test():
    post_rules()
    return "Test"

#create a route for submitting rules to the BC
