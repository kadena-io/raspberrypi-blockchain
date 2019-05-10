## Install dependencies

Make sure that you are running code with Python3.6.

    $ git clone https://github.com/kadena-io/raspberrypi-blockchain
    $ pip install --user pipenv
    $ cd raspberrypi-blockchain
    $ pipenv shell
    (raspberrypi-blockchain)$ pipenv install  # install requirements

raspberrypi-blockchain project uses [pypact](https://github.com/kadena-io/pypact) package so we need to install it:

    (raspberrypi-blockchain)$ pip3 install git+https://github.com/kadena-io/pypact.git

In the **env.sh** file change *PACT_SERVER* url with the url that pact server runs on. In the example I use my ip address as host:

    export PACT_SERVER="http://192.168.2.21:8081/api/v1/"

Before running the **logsensordata.py** script run **pact/scripts/env.sh** as follows:
    
    (raspberrypi-blockchain)$ source ./pact/scripts/env.sh
    (raspberrypi-blockchain)$ python logsensordata.py

### Run tests

    (raspberrypi-blockchain)$ python -m unittest -v
    
