import socket

def tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 8080))
    s.listen(5)
    print("App Server is listening on port 8080...")
    while True:
        conn, addr = s.accept()
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Received data", data.decode())

            response = "Error not implemented\n"
            conn.send(response.encode())
        conn.close()

