# Tcp Chat server

import socket, select
import random

def validate_data(sock, message):
    is_valid = True
    if (message[0] == 'STORE' and len(message) == 3):
        phone_num = message[2]
        go_ahead = False
        #message[2]= int(message[2])
        if (len(phone_num)==12):
            if (phone_num[3] == '-' and phone_num[7] == '-'):
                if (phone_num[0:3].isdigit() and phone_num[4:7].isdigit() and
                        phone_num[8:12].isdigit()):
                    if(not message[1].isdigit()):
                        go_ahead = True
        if (go_ahead):
            is_valid = True
        else:
            sock.send('Please enter in valid format <STORE Name Phone>\n')
            is_valid = False
    elif (message[0] == 'GET' and len(message) == 2):
        if (message[1].isdigit()):
            sock.send('Please enter in valid format <GET Name>\n')
            is_valid = False
        else:
            is_valid = True
    elif (message[0] == 'REMOVE' and len(message) == 2):
        if (message[1].isdigit()):
            sock.send('Please enter in valid format <REMOVE Name>\n')
            is_valid = False
        else:
            is_valid = True
    elif ((message[0] in ('GET', 'REMOVE') and len(message) != 2) or
         (message[0] == 'STORE' and len(message) != 3)):
        is_valid = False
        sock.send('Please enter in valid format\n')
    elif (message[0] in ('EXIT', 'QUIT') and len(message) == 1):
        sock.send('Disconnecting Client')
        sock.close()
        CONNECTION_LIST.remove(sock)
    else:
        is_valid = False
        sock.send('Please enter valid commands - STORE/GET/REMOVE\n')

    return is_valid

if __name__ == "__main__":

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = 'localhost'
    port = 54092
    server_socket.bind((host,port))
    #host = socket.gethostbyname(socket.gethostname())
    #server_socket.bind((host, 0))

    server_socket.listen(10)
    phonebook = {}  #Create an empty dictionary


    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)



    print "Chat server started at %s,%s" % (server_socket.getsockname())

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])


        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print  'Connections right now: %d' % len(CONNECTION_LIST)
                print "Client (%s, %s) connected" % addr,sockfd

            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    print 'Message from %s - %s' % (addr, data)

                    if data:
                        data_list = data.split()
                        valid = validate_data(sock, data_list)
                        if (data_list[0] == 'STORE' and valid):
                            phonebook[data_list[1]] = data_list[2]
                            sock.send('100 OK\n')
                        elif (data_list[0] == 'GET' and valid):
                            if data_list[1] in phonebook:
                                sock.send('200 %s\n' %phonebook[data_list[1]])
                            else:
                                sock.send('300 Not Found\n')
                        elif (data_list[0] == 'REMOVE' and valid):
                            if data_list[1] in phonebook:
                                del phonebook[data_list[1]]
                                sock.send('100 OK\n')
                            else:
                                sock.send('300 Not Found\n')
                        elif (data_list[0]  == 'EXIT' or data_list[0] == 'QUIT'):
                            sock.send('Disconnecting Client')
                            sock.close()
                    else:
                        sock.send('400 Bad request\n')
                except:
                    print "Client (%s, %s) is offline" % addr
                    print  'Connections right now: %d' % len(CONNECTION_LIST)
                    if sock in CONNECTION_LIST:
                        CONNECTION_LIST.remove(sock)
                    sock.close()
                    continue

    server_socket.close()