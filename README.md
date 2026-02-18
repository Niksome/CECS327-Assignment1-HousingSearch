# CECS Mini Housing Search Service
### Group members:
- Andrej Ermoshkin 
- Ashley Celis 
- Fortune Meya 

[Repository link](https://github.com/Niksome/CECS327-Assignment1-HousingSearch)


## How to run:
### Step 0: Setup
To get all the packages necessary for to run this project we recommend setting up a virtual environment like this:
1. Create a virtual environment: ```python -m venv <virtualEnvironmentName>```
2. Activate the virtual environment:
    - On Windows: ```<virtualEnvironmentName>\Scripts\activate```
    - On Linux/macOS: ```source <virtualEnvironmentName>/bin/activate```
3. Now just install all dependencies by running: ```pip install -r requirements.txt```
4. You can now quit the virtual environment by typing: ```deactivate```

### Step 1: Start Data Server
Command: ```python data_server.py```
Expected output: ```The data server listens on: 127.0.0.1:8081```

### Step 2: Start Application Server
Command: ```python app_server.py```
Expected output: 
```The application server listens on: 127.0.0.1:8080```
```The application server connects on:127.0.0.1:8081```

### Step 3: Start Client
Command: ```python client.py```
Expected output: ```The client connects to the application server on: 127.0.0.1:8080```


## Configuration Options:
`data_server.py` → binds to port 8081
`app_server.py` → binds to port 8080, connects to port 8081
`client.py` → connects to port 8080
