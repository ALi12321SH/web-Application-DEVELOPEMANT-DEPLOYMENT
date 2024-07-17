import socket
import threading
from scapy.all import *

def threaded(fn):
    def wrapper(*args, **kwargs):
        _thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        _thread.start()
        return _thread
    return wrapper

class HTTPProxy(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.stop = False

    @threaded
    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(4096).decode()
            print(f"Received request:\n{request}")
            

            first_line = request.split('\n')[0]
            url = first_line.split(' ')[1]

            http_pos = url.find("://")
            if http_pos == -1:
                temp = url
            else:
                temp = url[(http_pos+3):]

            port_pos = temp.find(":")
            webserver_pos = temp.find("/")
            if webserver_pos == -1:
                webserver_pos = len(temp)

            webserver = ""
            port = -1
            if (port_pos == -1 or webserver_pos < port_pos):
                port = 80
                webserver = temp[:webserver_pos]
            else:
                port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
                webserver = temp[:port_pos]

            proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_socket.connect((webserver, port))
            proxy_socket.send(request.encode())

            while True:
                data = proxy_socket.recv(4096)
                if len(data) > 0:
                    client_socket.send(data)
                else:
                    break

            proxy_socket.close()
            client_socket.close()
        except Exception as e:
            print(f"Error handling client: {e}")
            client_socket.close()

    def run(self):
        self.server.listen()
        print(f"Listening on {self.host}:{self.port}")

        while not self.stop:
            try:
                client_socket, addr = self.server.accept()
                print(f"Accepted connection from {addr}")
                self.handle_client(client_socket)
            except KeyboardInterrupt:
                self.stop = True
            except Exception as e:
                print(f"Exception: {e}")

if __name__ == "__main__":
    proxy = HTTPProxy("0.0.0.0", 8082)
    proxy.run()