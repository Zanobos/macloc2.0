# Development guideline

# Webserver

## Unix

### Setup environment

1) Download the packages needed
```sh
sudo apt-get -y update
sudo apt-get -y install git python3 python3-venv python3-dev
```
2) Setup the workspace
```sh
git clone https://github.com/Zanobos/macloc
cd macloc/webserver
echo -e "FLASK_APP=webserver.py\nFLASK_DEBUG=1\n" > ".flaskenv"
python3 -m venv venv
source venv/bin/activate
pip install -r app/doc/requirements.txt
flask db upgrade
```

### Useful commands

1) Start the server
```sh
source venv/bin/activate
flask run
``` 
2) Open a python terminal with everything ready
```sh
source venv/bin/activate
flask shell
``` 

# Webapp

## Unix

### Setup environment

1) Download the packages needed
```sh
sudo apt-get -y update
sudo apt-get -y install git npm
```
2) Setup the workspace
```sh
git clone https://github.com/Zanobos/macloc
cd macloc/webapp
sudo npm install -g npm@latest
npm install
```

### Useful commands

1) Serves the FE locally for testing and developing
```sh
npm run dev
``` 