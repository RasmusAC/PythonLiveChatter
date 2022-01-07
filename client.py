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
        root.quit()  # Lukker tkinter

#Håndtering af ordentlig afkobling.
def on_closing(event=None):                                                                             #Funktionen sørger for at lukke forbindelsen, hvis nu man klikker på det røde kryds.
    if isConnected == True:
        my_msg.set("/afslut")                                                                               #Skriver beskeden som lukker programmet
        send()                                                                                              #Sender beskeden.
    root.quit()  # Lukker tkinter

def init():
    global isConnected
    isConnected = False

#Tilslutning til server - SOCKET
def connect():
    global HOST
    global PORT
    global client_socket
    global BUFSIZ
    global ADDR
    global isConnected
    HOST = TkHOST.get()
    PORT = TkPORT.get()

    if not PORT:
        PORT = 33000  # Hvis man efterlader porten blank, så bruger den default porten.
    else:
        PORT = int(PORT)

    BUFSIZ = 1024  # Sætter en bufferstørrelse, hvor antallet er i bytes.
    ADDR = (HOST, PORT)  # Samler host og porten til en tuple.

    client_socket = socket(AF_INET, SOCK_STREAM)  # Starter serveren med en TCP protokol.

    try:
        client_socket.connect(ADDR)  # Serveren bliver bundet til computerens adresse.
        # Begynder at starte programmet.
        receive_thread = Thread(target=receive)  # Initialiserer multithreading for recieve funktionen.
        receive_thread.start()  # Den starter tråden.
        isConnected = True
    except:
        isConnected = False
        TkHOST.set("Forkert host eller port")
        TkPORT.set("Forkert host eller port")
        print("fejl i connect")

#Kalder init
init()

#Minimerer konsollen
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )

#Initialisering af TkInter
HEIGHT = 500
WIDTH = 750

root = tk.Tk()
root.minsize(WIDTH, HEIGHT)
root.maxsize(WIDTH, HEIGHT)
root.title("Corona chat")

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.place(relheight=1, relwidth=1)

frame_top = tk.Frame(canvas)
frame_top.place(rely=0, relx=0, relheight=0.15, relwidth=1)

frame_left = tk.Frame(canvas)
frame_left.place(rely=0.15, relx=0, relheight=0.85, relwidth=0.3)

frame_right = tk.Frame(canvas)
frame_right.place(rely=0.15, relx=0.3, relheight=0.85, relwidth=0.7)

#TOP-----------------------------------------------------------------------
titel = tk.Label(frame_top, text="Corona Chat", font=("Arial", 36))
titel.pack()

#VENSTRE------------------------------------------------------------------- 
frame_host = tk.Frame(frame_left)
frame_host.place(rely=0, relx=0, relheight=0.15, relwidth=1)

frame_port = tk.Frame(frame_left)
frame_port.place(rely=0.15, relx=0, relheight=0.15, relwidth=1)

frame_name = tk.Frame(frame_left)
frame_name.place(rely=0.30, relx=0, relheight=0.15, relwidth=1)

frame_btn = tk.Frame(frame_left)
frame_btn.place(rely=0.45, relx=0, relheight=0.15, relwidth=1)

hostLabel = tk.Label(frame_host, text="Host:")
hostLabel.place(rely=0.1, relx=0.025, relheight=0.4, relwidth=0.125)
TkHOST = tk.StringVar()
TkHOST.set("")
host_entry = tk.Entry(frame_host, textvariable=TkHOST)
host_entry.place(rely=0.5, relx=0.025, relheight=0.35, relwidth=0.975)

portLabel = tk.Label(frame_port, text="Port:")
portLabel.place(rely=0.1, relx=0.025, relheight=0.4, relwidth=0.125)
TkPORT = tk.StringVar()
TkPORT.set("")
port_entry = tk.Entry(frame_port, textvariable=TkPORT)
port_entry.place(rely=0.5, relx=0.025, relheight=0.35, relwidth=0.975)

nameLabel = tk.Label(frame_name, text="Navn:")
nameLabel.place(rely=0.1, relx=0.025, relheight=0.4, relwidth=0.14)
name_entry = tk.Entry(frame_name)
name_entry.place(rely=0.5, relx=0.025, relheight=0.35, relwidth=0.975)

afslut_button = tk.Button(frame_btn, text="Afslut", command=on_closing)
afslut_button.place(rely=0.1, relx=0.125, relheight=0.4, relwidth=0.3)
login_button = tk.Button(frame_btn, text="Login", command=connect)
login_button.place(rely=0.1, relx=0.572, relheight=0.4, relwidth=0.3)

#HØJRE-------------------------------------------------------------------
messages_frame = tk.Frame(frame_right)
scrollbar = tk.Scrollbar(messages_frame)
msg_list = tk.Listbox(messages_frame, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.place(rely=0, relx=0, relheight=1, relwidth=0.962)
messages_frame.place(rely=0.0, relx=0.025, relheight=0.7, relwidth=0.95)

frame_rightbund = tk.Frame(frame_right)
frame_rightbund.place(rely=0.72, relx=0.025, relheight=0.065, relwidth=0.95)

my_msg = tk.StringVar()
my_msg.set("")
entry_field = tk.Entry(frame_rightbund, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.place(rely=0.15, relx=0, relheight=0.7, relwidth=0.84)
send_button = tk.Button(frame_rightbund, text="Send", command=send)
send_button.place(rely=0.05, relx=0.85, relheight=0.9, relwidth=0.15)

#Sikkerhedsprotokol - TkInter
root.protocol("WM_DELETE_WINDOW", on_closing)                                                           #Protokol der kører 'on_closing', når man lukker TkInter vinduet.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Starter loop - TkInter
tk.mainloop()                                                                                           #Starter TkInter loopet.
