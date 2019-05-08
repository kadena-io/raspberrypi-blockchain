## Install dependencies

Make sure that you are running code with Python3.6

    $ pip install --user pipenv
    $ cd raspberrypi-blockchain
    $ pipenv shell
    $ pipenv install  # install requirements

Before running the script run **pact/scripts/env.sh** as follows:
    
    $ cd raspberrypi-blockchain
    $ source ./pact/scripts/env.sh
    $ python logsensordata.py

### Run tests

    (env)$ python -m unittest -v
    
