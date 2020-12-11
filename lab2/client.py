import socket
import sys
import argparse
import time
import threading
import datetime
import json

host = 'localhost'


def echo_client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    print("Connecting to %s port %s" % server_address)
    sock.connect(server_address)
    try:
        name = input("Select your name : ")
        num = input("Select your id : ")
        x = {"name": name, "id": num}
        send_json = json.dumps(x)
        print("Sending %s" % send_json)
        sock.sendall(send_json.encode())
        amount_received = 0
        amount_expected = len(send_json)
        print(amount_expected)
        while amount_received < amount_expected:
            data = sock.recv(1000)
            amount_received += len(data)
        print("Received: %s" % data.decode())
    finally:
        print("Closing connection to the server")
        sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)
