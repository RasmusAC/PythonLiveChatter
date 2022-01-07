#Socket modulet bruges til at forbinde de forskellige computere netværk.
from socket import AF_INET, socket, SOCK_STREAM
#Threading bruges til at kører flere ting på én gang.
from threading import Thread
#Datetime bruges til at få nuværende tid og dato.
from datetime import datetime
#Logging bruges til logfiler
import logging

logging.basicConfig(level=logging.INFO,format='%(message)s',handlers=[logging.FileHandler(str(datetime.utcnow().strftime('%Y_%m_%d')) + '.log'), logging.StreamHandler()])

#Håndtering af nye brugere
def accept_incoming_connections():                                                          #Funktionen som kan acceptere indgående forbindelser til serveren.
    while True:                                                                             #Loop som tjekker for indgående anmodninger til at forbinde til serveren.
        client, client_address = SERVER.accept()                                            #Accepterer forbindelsen for brugeren.
        #print("%s:%s har tilsluttet chatten." % client_address)                             #Skriver i server konsollen, at en bruger har forbundet til chatten.
        addresses[client] = client_address                                                  #Opbevare den brugerens adresseoplysninger.
        Thread(target=handle_client, args=(client,)).start()                                #Håndterer den brugeren (nedenstående funktion bliver kaldt).

#Håndtering af brugeren(e)
def handle_client(client):                                                                  #Funktionen som skal håndtere brugeren, og tager derfor 1 argument, som er brugeren.
    name = client.recv(BUFSIZ).decode("utf8")                                               #Gemmer brugerens nye navn.
    welcome = 'Velkommen %s!' % name                                                        #En velkomstbesked bliver gemt.
    client.send(bytes(welcome, "utf8"))                                                     #Sender velkomstbeskeden til den nye bruger.
    msg = "%s har tilsluttet sig chatten!" % name                                           #En besked til chatten gemt.
    broadcast(bytes(msg, "utf8"))                                                           #Sender beskeden.
    logging.info(str(datetime.now().strftime("[%H:%M:%S] ")) + str(msg))
    clients[client] = name                                                                  #Gemmer den nye brugers adresse og navn i en 'dictionary'.

    while True:                                                                             #Centrale loop for al komunikation.
        msg = client.recv(BUFSIZ)                                                           #Henter beskeden. Henter 'BUFSIZ' (1024 byte) af gangen, og kører igen hvis noget tekst mangler.
        if msg == bytes("/afslut", "utf8"):                                                  #Hvis brugeren ikke har skrevet /afslut, så udskriver den brugerens besked.
            logging.info(str(datetime.now().strftime("[%H:%M:%S] ")) + "%s har forladt chatten." % name)
            client.close()  # Lukker forbindelsen for brugeren.
            del clients[client]  # Sletter brugeren fra systemet.
            broadcast(bytes("%s har forladt chatten." % name, "utf8"))  # Fortæller brugerne at en bruger har forladt chatten.
            break
        elif msg == bytes("/disconnect", "utf8"):
            logging.info(str(datetime.now().strftime("[%H:%M:%S] ")) + "%s har forladt chatten." % name)
            client.close()  # Lukker forbindelsen for brugeren.
            del clients[client]  # Sletter brugeren fra systemet.
            broadcast(bytes("%s har forladt chatten." % name, "utf8"))  # Fortæller brugerne at en bruger har forladt chatten.
            break
        else:
            broadcast(msg, name + ": ")  # Udskriver brugerens navn og besked.
            user_msg = msg.decode("utf8")
            logging.info(str(datetime.now().strftime("[%H:%M:%S] ")) + str(name) + ": " + str(user_msg))

#Udsendelse af beskeder
def broadcast(msg, prefix=""):                                                              #Funktionen som udsender beskeder til alle i chatten. Argumentet prefix er så folk kan se hvem der sender beskeden.
    for sock in clients:                                                                    #Antallet af brugere den skal sende en besked ud til.
        sock.send(bytes(prefix, "utf8")+msg)                                                #Sender beskeden.


#Opsætter nogle variabler.
clients = {}                                                                                #Brugernes navn
addresses = {}                                                                              #Brugernes adresse (ip og port)

HOST = '192.168.0.119'#81'                                                                       #Hostens ip-adresse.
PORT = 33000                                                                                #Hostens port.
BUFSIZ = 1024                                                                               #Sætter en bufferstørrelse, hvor antallet er i bytes.
ADDR = (HOST, PORT)                                                                         #Samler host og porten til en tuple.

SERVER = socket(AF_INET, SOCK_STREAM)                                                       #Dette starter serveren med en TCP protokol.
SERVER.bind(ADDR)                                                                           #Her bliver serveren bundet til computerens adresse.

if __name__ == "__main__":
    SERVER.listen(5)                                                                        #Nægter adgang til andre forbindelser, hvis der har været 5 uaccepterede forbindelser.
    logging.info(str(datetime.now().strftime("[%H:%M:%S] ")) + "Succesfuld server opstart")
    logging.info(str(datetime.now().strftime("[%H:%M:%S] ")) + "HOST: " + str(HOST))
    logging.info(str(datetime.now().strftime("[%H:%M:%S] ")) + "PORT: " + str(PORT))
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)                              #Initialisere multithreading for accept funktionen.
    ACCEPT_THREAD.start()                                                                   #Den starter tråden.
    ACCEPT_THREAD.join()                                                                    #Joiner tråden således at den ikke går videre og koden og lukker serveren.
    SERVER.close()                                                                          #Lukker serveren.
