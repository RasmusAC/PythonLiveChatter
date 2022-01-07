#Socket modulet bruges til at forbinde de forskellige computere netværk.
from socket import AF_INET, socket, SOCK_STREAM
#Threading bruges til at kører flere ting på én gang.
from threading import Thread

#Håndtering af nye brugere
def accept_incoming_connections():                                                          #Funktionen som kan acceptere indgående forbindelser til serveren.
    while True:                                                                             #Loop som tjekker for indgående anmodninger til at forbinde til serveren.
        client, client_address = SERVER.accept()                                            #Accepterer forbindelsen for brugeren.
        print("%s:%s har tilsluttet serveren." % client_address)                            #Skriver i server konsollen, at en bruger har forbundet til serveren.
        client.send(bytes("Velkommen til chatten. Skriv dit navn og klik enter.", "utf8"))  #Skriver en besked til brugeren med utf8 format.
        addresses[client] = client_address                                                  #Opbevare den brugerens adresseoplysninger.
        Thread(target=handle_client, args=(client,)).start()                                #Håndterer den brugeren (nedenstående funktion bliver kaldt).

#Håndtering af brugeren(e)
def handle_client(client):                                                                  #Funktionen som skal håndtere brugeren, og tager derfor 1 argument, som er brugeren.
    name = client.recv(BUFSIZ).decode("utf8")                                               #Gemmer brugerens nye navn.
    welcome = 'Velkommen %s! Skriv {stop} for at afslutte.' % name                          #En velkomstbesked bliver gemt.
    client.send(bytes(welcome, "utf8"))                                                     #Sender velkomstbeskeden til den nye bruger.
    msg = "%s har tilsluttet sig chatten!" % name                                           #En besked til chatten gemt.
    broadcast(bytes(msg, "utf8"))                                                           #Sender beskeden.
    clients[client] = name                                                                  #Gemmer den nye brugers adresse og navn i en 'dictionary'.

    while True:                                                                             #Centrale loop for al komunikation.
        msg = client.recv(BUFSIZ)                                                           #Henter beskeden. Henter 'BUFSIZ' (1024 byte) af gangen, og kører igen hvis noget tekst mangler.
        if msg != bytes("{stop}", "utf8"):                                                  #Hvis brugeren ikke har skrevet {stop}, så udskriver den brugerens besked.
            broadcast(msg, name+": ")                                                       #Udskriver brugerens navn og besked.
        else:
            #client.send(bytes("{stop}", "utf8"))                                            #Ellers hvis brugeren har skrevet {stop}.
            client.close()                                                                  #Lukker forbindelsen for brugeren.
            del clients[client]                                                             #Sletter brugeren fra systemet.
            broadcast(bytes("%s har forladt chatten." % name, "utf8"))                      #Fortæller brugerne at en bruger har forladt chatten.
            break

#Udsendelse af beskeder
def broadcast(msg, prefix=""):                                                              #Funktionen som udsender beskeder til alle i chatten. Argumentet prefix er så folk kan se hvem der sender beskeden.
    for sock in clients:                                                                    #Antallet af brugere den skal sende en besked ud til.
        sock.send(bytes(prefix, "utf8")+msg)                                                #Sender beskeden.


#Opsætter nogle variabler.
clients = {}                                                                                #Brugernes navn
addresses = {}                                                                              #Brugernes adresse (ip og port)

HOST = '192.168.0.81'                                                                       #Hostens ip-adresse.
PORT = 33000                                                                                #Hostens port.
BUFSIZ = 1024                                                                               #Sætter en bufferstørrelse, hvor antallet er i bytes.
ADDR = (HOST, PORT)                                                                         #Samler host og porten til en tuple.

SERVER = socket(AF_INET, SOCK_STREAM)                                                       #Dette starter serveren med en TCP protokol.
SERVER.bind(ADDR)                                                                           #Her bliver serveren bundet til computerens adresse.

if __name__ == "__main__":
    SERVER.listen(5)                                                                        #Nægter adgang til andre forbindelser, hvis der har været 5 uaccepterede forbindelser.
    print("Venter på forbindelse fra bruger...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)                              #Initialisere multithreading for accept funktionen.
    ACCEPT_THREAD.start()                                                                   #Den starter tråden.
    ACCEPT_THREAD.join()                                                                    #Joiner tråden således at den ikke går videre og koden og lukker serveren.
    SERVER.close()                                                                          #Lukker serveren.
