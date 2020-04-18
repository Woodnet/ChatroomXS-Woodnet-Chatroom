from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s hat sich verbunden." % client_address)
        client.send(bytes("Willkommen beim Woodnet Chatroom! Gebe bitte deinen gewuenschten Namen ein und druecke Enter", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Willkommen %s! Wenn du den Chat verlassen willst gebe bitte {quit} ein.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s ist dem Chat beigetreten!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if (msg != bytes("{quit}", "utf8")):
            broadcast(msg, name+": ")
        else:
            #client.send(bytes("{quit}", "utf8"))
            del clients[client]
            print("%s hat den Chat verlassen." % name)
            broadcast(bytes("%s hat den Chat verlassen." % name, "utf8"))
            client.close()
            quit()


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


clients = {}
addresses = {}

HOST = 'localhost'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Warte auf Clients..")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
