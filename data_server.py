import pandas as pd
from socket import *

HOST = '127.0.0.1'
PORT = 8080
RAW_LIST = "RAW_LIST"
RAW_SEARCH = "RAW_SEARCH"
NEWLINE = "\n"
CITY_KEY = "city"
MAX_PRICE_KEY = "max_price"
EQUALS = "="
NO_COMMAND = "ERROR: This is not a valid command!\n"
NOT_ENOUGH_ARGS = "ERROR not enough arguments: RAW_SEARCH command requires a two arguments: cityname and max_price.\n"
TO_MUCH_ARGS = "ERROR too much arguments: RAW_SEARCH command requires a two arguments: cityname and max_price.\n"
MALFORMED_ARGS = "ERROR: malformed parameters.\n"
MISSING_PARAMS = "ERROR: missing parameters.\n"
PRICE_NOT_INT = "ERROR: max_price has to be an intiger but it appears not to be one.\n"

# Import listings data from json file
listings = pd.read_json('listings.json')

# Read one line and return it
def recv_input_line(conn) -> str:
    buf = b""
    while True:
        chunk = conn.recv(1)
        if not chunk:
            return ""
        if chunk == NEWLINE.encode():
            break
        buf += chunk
    return buf.decode()

def raw_list(conn):
    conn.sendall((listings.to_string() + NEWLINE).encode())

def raw_search_input_split(line):
    parts = line.split()

    # Checking for right amount of arguments
    if len(parts) < 3:
        conn.sendall(NOT_ENOUGH_ARGS.encode())
        return
    if len(parts) > 3:
        conn.sendall(TO_MUCH_ARGS.encode())
        return
    
    # Extracting the values for city and max_price
    params = {}
    for token in parts[1:]:
        if EQUALS not in token:
            conn.sendall(MALFORMED_ARGS.encode())
            return
        key, value = token.split(EQUALS, 1)
        params[key] = value
    
    city = params.get(CITY_KEY)
    max_price = params.get(MAX_PRICE_KEY)

    # Cheking if city and max_price are present to make sure that the creation worked
    if city is None or max_price is None:
        conn.sendall(MISSING_PARAMS.encode())
        return
    
    # Check if max_price is an intiger
    try:
        max_price = int(max_price)
    except:
        conn.sendall(PRICE_NOT_INT.encode())
        return
    
    return city, max_price

def raw_search(conn, line):
    try:
        city, max_price = raw_search_input_split(line)
    except:
        return
    
    findings = listings.loc[(listings[CITY_KEY] == city) & (listings[MAX_PRICE_KEY] <= max_price)]
    conn.sendall((findings.to_string() + NEWLINE).encode())

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
while True:
    (conn, addr) = s.accept()
    try:
        line = recv_input_line(conn)
        if not line: 
            continue
        
        if line == RAW_LIST:
            raw_list(conn)
        if line.startswith(RAW_SEARCH):
            raw_search(conn, line)
        else:
            conn.send(NO_COMMAND.encode())
    finally:
        conn.close()    