from tkinter import Canvas
import tkthread; tkthread.patch()

import customtkinter
import PIL
from tkintermapview import TkinterMapView
from PIL import Image,ImageTk
import os
from serial.tools import list_ports
import serial
import threading
import time
from threading import *



customtkinter.set_default_color_theme("blue")




APP_NAME = "Batonome GUI"
WIDTH = 800
HEIGHT = 500
app = customtkinter.CTk()  # create CTk window like you do with the Tk window


#app.title(APP_NAME)
app.geometry(str(WIDTH) + "x" + str(HEIGHT))
app.minsize(WIDTH, HEIGHT)

app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.bind("<Command-q>", app.on_closing)
app.bind("<Command-w>", app.on_closing)
app.createcommand('tk::mac::Quit', app.on_closing)

#Liste les ports COm disponible :
port_tuple = ()
listPortName = []
#listPortInit=()
com = "COM?"
            
        
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/Icons")
gps_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "GPS.png")),
                                            dark_image=Image.open(os.path.join(image_path, "GPS.png")), size=(20, 20))
navigation_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "navigation.png")),
                                            dark_image=Image.open(os.path.join(image_path, "navigation.png")), size=(20, 20))

disconnected_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "disconnected.png"))
                                                , dark_image=Image.open(os.path.join(image_path, "disconnected.png")), size=(30, 30))

marker_list = []
#InitZone
initZoneValue = False
listeGpsPoints = []
baliseState = False
baliseGPSCordinate = (0,0)
connectBato = False
xbee = None
sendDemande = False

# ============ create two CTkFrames ============

# grid_columnconfigure(0, weight=0)
# grid_columnconfigure(1, weight=0)
# grid_columnconfigure(2, weight=0)
# grid_rowconfigure(2, weight=1)

app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=0)
app.grid_rowconfigure(1, weight=0)
app.grid_rowconfigure(2, weight=1)



#Create the header frame
frame_header = customtkinter.CTkFrame(height=50, corner_radius=0,fg_color="#2b2b2b")
frame_header.grid(row=0, column=0,columnspan=2, padx=0, pady=0, sticky="nsew")

       
        

#Create the log frame
frame_log = customtkinter.CTkFrame(height=50, corner_radius=0, fg_color=None)
frame_log.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")
frame_log.grid_columnconfigure(0, weight=1)
       # frame_log.rowconfigure(0, weight=1)


# Create the App frame
frame_app = customtkinter.CTkFrame(corner_radius=0,fg_color=None)
frame_app.grid(row=2, column=0, padx=0, pady=0,sticky="nsew")
frame_app.grid_columnconfigure(0, weight=0)
frame_app.grid_columnconfigure(1, weight=1)
frame_app.grid_rowconfigure(0, weight=1)


#Create the nav_frame
frame_nav = customtkinter.CTkFrame(master=frame_app, width=100, corner_radius=0, fg_color=None)
frame_nav.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        

#Create the seting_frame
frame_setting = customtkinter.CTkFrame(master=frame_app, width = app.WIDTH, corner_radius=0)
frame_setting.grid_columnconfigure(0, weight=0)
frame_setting.grid_columnconfigure(1, weight=1)
frame_setting.grid_rowconfigure(0, weight=1)

frame_setting.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

# #create the navigation frame
frame_navigation = customtkinter.CTkFrame(master=frame_app, corner_radius=0,fg_color = "#585858")
frame_navigation.grid_columnconfigure(1, weight=1)
frame_navigation.grid_rowconfigure(0, weight=1)

        
#Create the left frame settings
frame_left = customtkinter.CTkFrame(master=frame_setting, width=100, corner_radius=0,fg_color = "#585858")
frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

#create the right frame settings
frame_right = customtkinter.CTkFrame(master=frame_setting, width=1200, corner_radius=0,fg_color = "#585858")
frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

# ============ header ============

frame_header.grid_columnconfigure(1, weight=1)
frame_header.grid_columnconfigure(0, weight=1)
frame_header.grid_rowconfigure(0, weight=1)

frame_header_left= customtkinter.CTkFrame(master=frame_header, corner_radius=0,height = 50 ,width = 400, fg_color=None)
frame_header_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
frame_header_right= customtkinter.CTkFrame(master=frame_header,  corner_radius=0,height = 50, fg_color=None)
frame_header_right.grid(row=0, column=1, padx=0, pady=0, sticky="nse")

        

# #Ajout du bouton connect
button_connect = customtkinter.CTkButton(frame_header_right, image=disconnected_image,text=None,width=60, height=30 ,fg_color="red", hover_color = "#ff2700",command = app.connect)
button_connect =  button_connect.grid(row=0, column=1, padx=(20, 20), pady=(10, 0),sticky="nse")
#reduire la taille du bouton
        

button_COM = customtkinter.CTkOptionMenu(frame_header_right, values=listPortName,width=90, height=30, command=app.majPortCom)
button_COM.grid(row=0, column=0, padx=(20, 20), pady=(10, 0),sticky="nse")
# ============ log ============
LogTextbox = customtkinter.CTkTextbox(master=frame_log, height=50,corner_radius=0,text_color="white", fg_color="black" ,state = "normal")
LogTextbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

LogTextbox.insert("0.0", "Log...")  # insert at line 0 character 0
LogTextbox = LogTextbox.get("0.0", "end")  # get text from line 0 character 0 till the end

# ============ frame_app ============

# ============ frame_nav ============

#Add Button settings
button_settings = customtkinter.CTkButton(frame_nav, corner_radius=0, height=40, border_spacing=10, text="Settings",image = gps_image,
                                            fg_color="transparent",text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        anchor="w", command=app.settings_button_event)
button_settings.grid(row=0, column=0, padx=0, pady=0, sticky="ew")

#Add Button Navigation
button_navigation = customtkinter.CTkButton(frame_nav, corner_radius=0, height=40, border_spacing=10, text="Navigation", image = navigation_image,
                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                            anchor="w", command=app.navigation_button_event)
button_navigation.grid(row=1, column=0, padx=0, pady=0, sticky="ew")

       
        

# ============ frame_left ============

frame_left.grid_rowconfigure(3, weight=1)
    #Ajouter une image dans le bouton

        
imageLock = customtkinter.CTkImage(light_image=Image.open("C://Users//scant//Dev//Batonome//Batonome-GUI//media//lock.png"),
                            dark_image=Image.open("C://Users//scant//Dev//Batonome//Batonome-GUI//media//lock.png"),
                            size=(20, 20))

imageUnLock = customtkinter.CTkImage(light_image=Image.open("C://Users//scant//Dev//Batonome//Batonome-GUI//media//unlock.png"),
                            dark_image=Image.open("C://Users//scant//Dev//Batonome//Batonome-GUI//media//unlock.png"),
                            size=(20, 20))

button_1 = customtkinter.CTkButton(master=frame_left,text="Zone Nav",image=imageUnLock, command=app.initZone)
button_1.grid(pady=(60, 0), padx=(20, 20), row=1, column=0)


frameBaliseGPS = customtkinter.CTkFrame(master=frame_left, fg_color="transparent",width=150, corner_radius=0)
frameBaliseGPS.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")
frameBaliseGPS.grid_rowconfigure(1, weight=1)
        
#Bouton pour mettre à jour la balise
button_MajBalise = customtkinter.CTkButton(master=frameBaliseGPS,text="Balise",image = imageUnLock,command = app.baliseGPS)
button_MajBalise.grid(pady=(30, 0), padx=(20, 20), row=0, column=0)

#Zone de texte popur stocker les coordonnées GPS de la balise
textBaliseLon = customtkinter.CTkTextbox(master=frameBaliseGPS, width=130, height=1)
textBaliseLon.grid(pady=(5, 0), padx=(20, 20), row=1, column=0)

#Zone de texte popur stocker les coordonnées GPS de la balise
textBaliseLat = customtkinter.CTkTextbox(master=frameBaliseGPS, width=130, height=1)
textBaliseLat.grid(row=3, column=0, padx=(20, 20), pady=(10, 0))



map_label = customtkinter.CTkLabel(frame_left, text="Tile Server:", anchor="w")
map_label.grid(pady=(5, 20), padx=(20, 20), row=3, column=0)
map_option_menu = customtkinter.CTkOptionMenu(frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"], command=app.change_map)
map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

# Bouton pour envoyer les infos au bateau
button_SendBoat = customtkinter.CTkButton(master=frameBaliseGPS,text="Syncronisation")
button_SendBoat.grid(row=5, column=0, padx=(20, 20), pady=(10, 0))

# ============ frame_right ============

frame_right.grid_rowconfigure(1, weight=1)
frame_right.grid_rowconfigure(0, weight=0)
frame_right.grid_columnconfigure(0, weight=1)
frame_right.grid_columnconfigure(1, weight=0)
frame_right.grid_columnconfigure(2, weight=1)

map_widget = TkinterMapView(frame_right, corner_radius=0)
map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

entry = customtkinter.CTkEntry(master=frame_right,
                                    placeholder_text="type address")
entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
entry.bind("<Return>", app.search_event)

button_5 = customtkinter.CTkButton(master=frame_right,
                                        text="Search",
                                        width=90,
                                        command=app.search_event)
button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

map_widget.add_left_click_map_command(app.left_click_event)

# Set default values
map_widget.set_address("Berlin")
map_option_menu.set("OpenStreetMap")
button_COM.set("COM?")

app.start()
        
    
def settings_button_event():
    select_frame_by_name("settings")

def navigation_button_event():
    select_frame_by_name("navigation")

def select_frame_by_name( name):
    # set button color for selected button
    button_settings.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")
    button_navigation.configure(fg_color=("gray75", "gray25") if name == "navigation" else "transparent")

    # show selected frame
    if name == "settings":
        frame_setting.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
    else:
        frame_setting.grid_forget()
    if name == "navigation":
        frame_navigation.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
    else:
        frame_navigation.grid_forget()

def search_event(event=None):
    map_widget.set_address(entry.get())

def baliseGPS(event=None):
    if (baliseState==False):
        baliseState = True
        textBaliseLat.configure(state="disabled")
        textBaliseLon.configure(state="disabled")
        #Recupere les coordonnées GPS de la balise
        #baliseGPSCordinate = (float(textBaliseLat.get("0.0", "end")) , float(textBaliseLon.get("0.0", "end")))
        #Positionne une balise bleue
        #markerBaliseGPS = map_widget.set_marker(baliseGPSCordinate[0], baliseGPSCordinate[1])
        #Maj cadenas
        button_MajBalise.configure(image = imageLock)

    else:
        baliseState = False
        textBaliseLat.configure(state="normal")
        textBaliseLon.configure(state="normal")
        #Maj Cadena
        button_MajBalise.configure(image = imageUnLock)
        #Suprime la balise bleue
        app.markerBaliseGPS.delete()


def left_click_event(coordinates_tuple):
    print(initZoneValue)
    print(baliseState)
    if (initZoneValue==False):
        print("Left click event with coordinates:", coordinates_tuple)
        marker_list.append(map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1]))
        listeGpsPoints.append(coordinates_tuple)
        print(listeGpsPoints)
    else:
        if (baliseState==False):
            #baliseGPS()
            markerBaliseGPS = map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1])
            baliseGPSCordinate = (float(coordinates_tuple[0]) , float(coordinates_tuple[0]))
            #Positionne les info GPS dans les textboxes
            textBaliseLat.delete("0.0", "end")
            textBaliseLon.delete("0.0", "end")
            textBaliseLat.insert("0.0", baliseGPSCordinate[0])
            textBaliseLon.insert("0.0", baliseGPSCordinate[1])
            baliseGPS()
            


def initZone( event=None):
    if(initZoneValue == False):
        initZoneValue = True
        polygon_1 = map_widget.set_polygon(listeGpsPoints, fill_color=None,  outline_color="red",  border_width=12, name="Zone de navigation")
        button_1.configure(image=imageLock)
    else:
        initZoneValue = False
        polygon_1.delete()
        listeGpsPoints.clear()
        button_1.configure(image=imageUnLock)
        clear_marker_event()

    

def clear_marker_event():
    for marker in marker_list:
        marker.delete()

def listPortInit():
    #Erase the tuple
    listPortName.clear()
    listPort = list_ports.comports()
    listPortName = []
    for port in listPort:
        listPortName.append(port.device)

def addLog(text):
    countLine = 1
    #LogTextbox.insert("0.0", text)  # insert at line 0 character 0
    countLine = countLine + 1

def connect():
    if(com == "COM?"):
        print("Veuillez selectionner un port COM valide")
        addLog("Veuillez selectionner un port COM valide")
    else:
        initCOM()
        print("Connexion au port COM : " + com)

        addLog("Connexion au port COM : " + com)
        addLog("Veuillez patienter...")
        addLog("")
        connectBato = True
        thread_run()
        #device = XBeeDevice(com, 9600)
        sendDataToBoat("Batonome Vaincra")


def sendDataToBoat(textToSend):
    print("Envoi de : " + textToSend)
    # device.open()
    # device.send_data_broadcast(textToSend)
    # device.close()

def majPortCom(new_com: str):
    com = new_com
    addLog("Port COM selectionné : ")
    print(com)


def change_appearance_mode( new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

def change_map( new_map: str):
    if new_map == "OpenStreetMap":
        map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
    elif new_map == "Google normal":
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    elif new_map == "Google satellite":
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

def initCOM():
    # Ouvre la liaison série sur le port sélectionné à une vitesse de 9600 bauds
    xbee = serial.Serial(com, 9600)
    # Attend 2 secondes que le module XBee soit prêt
    #time.sleep(1)
    # Envoie la chaîne de caractères "4" au module XBee
    #xbee.write(b'4')
    # Attend 2 secondes que le module XBee traite la commande
    #time.sleep(1)
    # Ferme la liaison série
    # xbee.close()

def thread_run(): threading.Thread(target=work).start()
def work():
    print("in thread")
    while True:
        print("in while")
        if(connectBato == True):
            data = "4"
            xbee.write(data.encode())
            print("send 4")
            time.sleep(1)

            #si donnee sur le port serie
            data = app.xbee.read()
            if(data):
                print(data)


    

def on_closing(event=0):
    app.destroy()

def start():
    app.mainloop()
        

 

                
def threading1():
    t1=Thread(target=work)
    t1.start()














   
    
