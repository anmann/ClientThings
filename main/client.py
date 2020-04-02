import socket
import sys  

def tcpc():
    tclient = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        host = input("Target host: ")
        port = input("Target port: ")
        try:
            tclient.connect((host,int(port)))
        except socket.gaierror as err:
            print(str(err))
            print("Make sure you typed the host and port correctly!\n")
            tcpc()
        except ValueError:
            print(ValueError)
            print("Make sure you typed the host and port correctly!\n")
            tcpc()

        while 1:

            response = tclient.recv(2046)

            print(response)

            if len(response):
                print("Data successfully received")
            else:
                print("No further data received")

            tsend = input(">>> ")
            tclient.send(tsend)


    except KeyboardInterrupt:
        print("\nClosing program...\n")
        tclient.close()
        sys.exit()
    except socket.error:
        print(socket.error)
        print("\nclosing program...\n")
        tclient.close()
        sys.exit()
    except:
        print("\nclosing program...\n")
        tclient.close()
        sys.exit()

tcpc()
