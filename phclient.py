#AMAR 123456789

import socket, select, string, sys

def prompt() :
    sys.stdout.write('>')
    sys.stdout.flush()


#main function
if __name__ == "__main__":

    #if(len(sys.argv) < 3) :
        #print 'Usage : python telnet.py hostname port'
        #sys.exit()

    #print sys.argv
    #host = sys.argv[1]
    #port = int(sys.argv[2])

    host = 'localhost'
    port = 54097

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. Start sending messages'
    prompt()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])


        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if data == 'Disconnecting Client':
                    print '\nDisconnected from server'
                    sys.exit()
                else :
                    #print data
                    if data:
                        sys.stdout.write(data)
                        prompt()

            #user entered a message
            else:
                msg = sys.stdin.readline()
                strmsg = str(msg)
                if not msg or msg.strip == '':
                    print('Please enter Data')
                    prompt()
                elif (len(strmsg) > 0):
                #elif (strmsg.startswith('STORE') or strmsg.startswith('GET') or strmsg.startswith('REMOVE')
                      #or strmsg.startswith('EXIT') or strmsg.startswith('QUIT')):
                    s.send(msg)
                    prompt()




