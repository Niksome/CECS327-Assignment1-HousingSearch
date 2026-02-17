import socket

cache = {}

#  connects to the data server
def ask_data(cmd):
    ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ds.connect(("127.0.0.1", 8080))
    ds.sendall((cmd + "\n").encode())

    buf = ""
    lines = []

    # looking for END
    while True:
        data = ds.recv(1024)
        if not data:
            break

        buf += data.decode(errors="replace")

        while "\n" in buf:
            line, buf = buf.split("\n", 1)
            line = line.strip()
            if line != "":
                lines.append(line)

            if line == "END":
                ds.close()
                return lines

    ds.close()
    return lines

# logging function
def log(x):
    f = open("app_server.log", "a")
    f.write(x + "\n")
    f.close()

def sort_rule(item):
    return item["price"], -item["bedrooms"]

def tcp_server():

    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind to port 8081
    s.bind(("127.0.0.1", 8081))
    s.listen(5)

    print("app server running on 8081")

    while True:
        conn, addr = s.accept()
        print("client connected", addr)

        buf = ""
        quit_now = False

        while not quit_now:
            data = conn.recv(1024)
            if not data:
                break

            buf += data.decode(errors="replace")

            # process complete lines
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                line = line.strip()

                if line == "":
                    continue

                log("C->A " + line)
                # handle quit
                if line == "QUIT":
                    quit_now = True
                    break

                # check cache first
                if line in cache:
                    conn.sendall(cache[line].encode())
                    log("A->C cache used")
                    continue

                parts = line.split()

                # handle list
                if parts[0] == "LIST" and len(parts) == 1:
                    ds_lines = ask_data("RAW_LIST")
                    log("A->D RAW_LIST")

                # handle search
                elif parts[0] == "SEARCH":

                    city = None
                    max_price = None

                    for t in parts[1:]:
                        if t.startswith("city="):
                            city = t.split("=")[1]
                        elif t.startswith("max_price="):
                            try:
                                max_price = int(t.split("=")[1])
                            except:
                                max_price = None

                    # check for invalid search
                    if city is None or max_price is None:
                        conn.sendall(b"ERROR invalid SEARCH syntax\n")
                        log("A->C search error")
                        continue

                    ds_lines = ask_data("RAW_SEARCH city=" + city + " max_price=" + str(max_price))
                    log("A->D RAW_SEARCH")

                else:
                    conn.sendall(b"ERROR unknown command\n")
                    log("A->C unknown command")
                    continue

                # check data server response
                if not ds_lines:
                    conn.sendall(b"ERROR data server no response\n")
                    log("A->C data error")
                    continue

                if ds_lines[0].startswith("ERROR"):
                    conn.sendall((ds_lines[0] + "\n").encode())
                    log("A->C data server error")
                    continue

                # parse items
                items = []

                for l in ds_lines[1:]:
                    if l == "END":
                        break

                    d = {}
                    for p in l.split(";"):
                        if "=" in p:
                            pair = p.split("=")
                            d[pair[0].strip()] = pair[1].strip()

                    try:
                        d["id"] = int(d["id"])
                        d["price"] = int(d["price"])
                        d["bedrooms"] = int(d["bedrooms"])
                    except:
                        continue

                    items.append(d)

                # sort results
                items = sorted(items, key=sort_rule)

                # build response
                out = []
                out.append("RESULT " + str(len(items)))

                for x in items:
                    line_out = "id=" + str(x["id"]) + ";city=" + x["city"] + ";address=" + x["address"] + ";price=" + str(x["price"]) + ";bedrooms=" + str(x["bedrooms"])
                    out.append(line_out)

                out.append("END")

                resp = "\n".join(out) + "\n"

                # save in cache
                cache[line] = resp

                # send to client
                conn.sendall(resp.encode())
                log("A->C OK")

        conn.close()
        print("connection closed")

tcp_server()
