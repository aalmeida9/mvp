Recommended project setup:
git clone https://github.com/aalmeida9/mvp.git\
cd mvp\
python3 -m venv venv\
source venv/bin/activate\
pip install -e .\

To run the actual web server application (use different terminal):\
export FLASK_APP=run.py\
export FLASK_ENV=development\
flask run\

To-dos (there's plenty more):
* Either integrate node_server into bc or define routes to access info on node_server
* Define routes for updating flows, Mac-table, etc on Ryu controller
* Create user friendly interface

Blockchain based on this repository: https://github.com/satwikkansal/python_blockchain_app/tree/ibm_blockchain_post\
To run the Blockchain (node_server):\
export FLASK_APP=node_server.py\
flask run --port 8000\
