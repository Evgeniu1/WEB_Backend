import socket
import sys
import argparse
import time
import threading
import datetime
import json

host = 'localhost'
data_payload = 2048
backlog = 5

send_code = False
cycle = False
list_user = [] 
need_time = 12
data_timer = ""  


def waiting():  
    global data_timer
    global send_code
    data_timer = str(datetime.datetime.now())
    time.sleep(need_time)
    send_code = True


def echo_server(port):
    global cycle
    global send_code
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    server_address = (host, port) 
    print("Starting up echo server  on %s port %s" % server_address)
    sock.bind(server_address)
    sock.listen(backlog)  
    while 1:  
        print("Waiting to receive message from client")
        cycle = True
        client, address = sock.accept()  
        data = client.recv(data_payload)
        dict_data = (json.loads(data.decode()))  
        list_user.append(dict_data['name'])
        x = threading.Thread(target=waiting)
        x.start()
        dict_data["time-connect"] = str(datetime.datetime.now())
        dict_data["time-timer"] = data_timer
        send_json = json.dumps(dict_data)
        print("Data: %s" % send_json)
        cycle = False
        while cycle == False:  
            if send_code == True:
                client.send(send_json.encode())  
                print("sent %s bytes back to %s" % (data, address))
                break
        send_code = False
    client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)  
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)
