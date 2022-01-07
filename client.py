#ctypes bruges til at minimere consolen
import ctypes
#Socket modulet bruges til at forbinde de forskellige computere netværk.
from socket import AF_INET, socket, SOCK_STREAM
#Threading bruges til at kører flere ting på én gang.
from threading import Thread
#TkInter bruges til at skabe en GUI
import tkinter as tk

#Håndtering af modtaget beskeder.
def receive():                                                                                          #Funktionen som gør at beskeder der er modtaget bliver vist i chatten.
    while True:                                                                                         #Et uendelighedsloop som hele tiden skal tjekke om der er kommet nye beskeder.
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")                                             #'.recv' gør at den venter på at modtage en besked, og går ikke videre i koden før.
            msg_list.insert(tk.END, msg)                                                                #Tilføljer beskeden til en liste.
        except OSError:                                                                                 #Et lille sikkerhedsnet i tilfælde af en bruger kobler af.
            break

#Håndtering af afsendte beskeder.
def send(event=None):                                                                                   #Funktionen som sørger for at sende ens besked ind til serveren som sender det ud til de andre.
    msg = my_msg.get()                                                                                  #Gemmer brugerens besked i en variabel.
    my_msg.set("")                                                                                      #Rydder inputfeltet.
    client_socket.send(bytes(msg, "utf8"))                                                              #Sender beskeden til serveren.
    if msg == "/afslut": 
        client_socket.close()                                                                           #Lukker forbindelsen
        root.quit()                                                                                     #Lukker tkinter

#Håndtering af ordentlig afkobling.
def on_closing(event=None):                                                                             #Funktionen sørger for at lukke forbindelsen, hvis nu man klikker på det røde kryds.
    my_msg.set("/afslut")                                                                               #Skriver beskeden som lukker programmet
    send()                                                                                              #Sender beskeden.

#Tilslutning til server - SOCKET
while True:
    HOST = input('Host: ')                                                                              #Indtastning af ip-adresse.
    PORT = input('Port: ')                                                                              #Indtastning af port.

    if not PORT:
        PORT = 33000                                                                                    #Hvis man efterlader porten blank, så bruger den default porten.
    else:
        PORT = int(PORT)

    BUFSIZ = 1024                                                                                       #Sætter en bufferstørrelse, hvor antallet er i bytes.
    ADDR = (HOST, PORT)                                                                                 #Samler host og porten til en tuple.

    client_socket = socket(AF_INET, SOCK_STREAM)                                                        #Starter serveren med en TCP protokol.

    try:
        client_socket.connect(ADDR)                                                                     #Serveren bliver bundet til computerens adresse.
        break
    except:
        print("fejl i host")
        input()

ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )                         #Minimere consolen.

#Initialisering af TkInter
root = tk.Tk()                                                                                          #Laver et vindue
root.title("Corona chat")                                                                               #Titel på vindue
messages_frame = tk.Frame(root)                                                                         #Laver en ramme til bedre organisering.

#Chat felt - TkInter
scrollbar = tk.Scrollbar(messages_frame)                                                                #Laver en scrollbar
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)                #Laver et felt til beskederne.
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)                                                                #Placerer scrollbaren og fortæller at den skal være i højre side, og fylde vertikalt.
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)                                                               #Placerer beskedfeltet og fortæller at den skal være i venstre side, og fylde horisontalt og vertikalt.
msg_list.pack()                                                                                         #Placerer hele beskedfeltet.
messages_frame.pack()                                                                                   #Placerer rammen.

#Brugerens inputfelt - TkInter
my_msg = tk.StringVar()                                                                                 #Laver en variabel til at gemme brugerens input.
my_msg.set("")  #Gør variablen tom
entry_field = tk.Entry(root, textvariable=my_msg)                                                       #Laver et inputfelt.
entry_field.bind("<Return>", send)                                                                      #Sender beskeden, når man klikker enter.
entry_field.pack()                                                                                      #Placerer inputfeltet.
send_button = tk.Button(root, text="Send", command=send)                                                #Laver en knap som kan sende beskeden.
send_button.pack()                                                                                      #Placerer knappen.

#Sikkerhedsprotokol - TkInter
root.protocol("WM_DELETE_WINDOW", on_closing)                                                           #Protokol der kører 'on_closing', når man lukker TkInter vinduet.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Begynder at starte programmet.
receive_thread = Thread(target=receive)                                                                 #Initialisere multithreading for recieve funktionen.
receive_thread.start()                                                                                  #Den starter tråden.

#Starter loop - TkInter
tk.mainloop()                                                                                           #Starter TkInter loopet.
