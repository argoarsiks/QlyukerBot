# Qlyuker bot for telegram mini app


## Functions
|       Functionality                   |Status|
|---------------------------------------|------|
|       Multistreaming                  |✅|
|       Binding proxy to session        |🔄|
|       Automatic booster upgrades      |✅|
|       Pyrogram .session compatibility |✅|


## Quick Start

### Getting API keys
1. Go to [**my.telegram.org**](https://my.telegram.org/auth).
2. Log in using your phone number.
3. Select "Api development tools" and fill in the form
4. Write API_ID and API_HASH in the .env file

### Installation
Download the repository
```shell
git clone https://github.com/argoarsiks/QlyukerBot.git
cd QlyukerBot
```

## Windows manual installation
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Linux manual installation
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```


You can also use arguments at startup
```shell
python3 main.py -a 1
# or
python3 main.py -a 2
```
1 - Create session
2 - Run bot