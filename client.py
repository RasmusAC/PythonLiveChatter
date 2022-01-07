#ctypes bruges til at minimere consolen
import ctypes
#Socket modulet bruges til at forbinde de forskellige computere netværk.
from socket import AF_INET, socket, SOCK_STREAM
#Threading bruges til at kører flere ting på én gang.
from threading import Thread
#TkInter bruges til at skabe en GUI
import tkinter

#Håndtering af modtaget beskeder.
def receive():                                                                                          #Funktionen som gør at beskeder der er modtaget bliver vist i chatten.
    while True:                                                                                         #Et uendelighedsloop som hele tiden skal tjekke om der er kommet nye beskeder.
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")                                             #'.recv' gør at den venter på at modtage en besked, og går ikke videre i koden før.
            msg_list.insert(tkinter.END, msg)                                                           #Tilføljer beskeden til en liste.
        except OSError:                                                                                 #Et lille sikkerhedsnet i tilfælde af en bruger kobler af.
            break

#Håndtering af afsendte beskeder.
def send(event=None):                                                                                   #Funktionen som sørger for at sende ens besked ind til serveren som sender det ud til de andre.
    msg = my_msg.get()                                                                                  #Gemmer brugerens besked i en variabel.
    my_msg.set("")                                                                                      #Rydder inputfeltet.
    client_socket.send(bytes(msg, "utf8"))                                                              #Sender beskeden til serveren.
    if msg == "{stop}": 
        client_socket.close()                                                                           #Lukker forbindelsen
        top.quit()                                                                                      #Lukker tkinter

#Håndtering af ordentlig afkobling.
def on_closing(event=None):                                                                             #Funktionen sørger for at lukke forbindelsen, hvis nu man klikker på det røde kryds.
    my_msg.set("{stop}")                                                                                #Skriver beskeden som lukker programmet
    send()                                                                                              #Sender beskeden.

#Tilslutning til server - SOCKET
HOST = input('Enter host: ')                                                                            #Indtastning af ip-adresse.
PORT = input('Enter port: ')                                                                            #Indtastning af port.

if not PORT:
    PORT = 33000                                                                                        #Hvis man efterlader porten blank, så bruger den default porten.
else:
    PORT = int(PORT)

ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )                         #Minimere consolen.

BUFSIZ = 1024                                                                                           #Sætter en bufferstørrelse, hvor antallet er i bytes.
ADDR = (HOST, PORT)                                                                                     #Samler host og porten til en tuple.

client_socket = socket(AF_INET, SOCK_STREAM)                                                            #Dette starter serveren med en TCP protokol.
client_socket.connect(ADDR)                                                                             #Her bliver serveren bundet til computerens adresse.

#Initialisering af TkInter
top = tkinter.Tk()                                                                                      #Laver et vindue
top.title("Corona chat")                                                                                #Titel på vindue
messages_frame = tkinter.Frame(top)                                                                     #Laver en ramme til bedre organisering.

#Chat felt - TkInter
scrollbar = tkinter.Scrollbar(messages_frame)                                                           #Laver en scrollbar
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)           #Laver et felt til beskederne.
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)                                                      #Scrollbaren skal være i højre side, og fylde vertikalt.
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)                                                     #Beskedfeltet skal være i venstre side, og fylde horisontalt og vertikalt.
msg_list.pack()                                                                                         #Organisere widgets før de bliver placeret.
messages_frame.pack()                                                                                   #Organisere widgets før de bliver placeret.

#Brugerens inputfelt - TkInter
my_msg = tkinter.StringVar()                                                                            #Laver en variabel til at gemme brugerens input.
my_msg.set("")  #Gør variablen tom
entry_field = tkinter.Entry(top, textvariable=my_msg)                                                   #Laver et inputfelt.
entry_field.bind("<Return>", send)                                                                      #Sender beskeden, når man klikker enter.
entry_field.pack()                                                                                      #Organisere widgets før de bliver placeret.
send_button = tkinter.Button(top, text="Send", command=send)                                            #Laver en knap som kan sende beskeden.
send_button.pack()                                                                                      #Organisere widgets før de bliver placeret.

#Sikkerhedsprotokol - TkInter
top.protocol("WM_DELETE_WINDOW", on_closing)                                                            #Protokol der kører 'on_closing', når man lukker TkInter vinduet.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Begynder at starte programmet.
receive_thread = Thread(target=receive)                                                                 #Initialisere multithreading for recieve funktionen.
receive_thread.start()                                                                                  #Den starter tråden.

#Starter loop - TkInter
tkinter.mainloop()                                                                                      #Starter TkInter loopet.
