from ctypes import sizeof
import sys
from tkinter import Canvas
import threading

import customtkinter
import PIL
from tkintermapview import TkinterMapView
from PIL import Image,ImageTk
import os
from serial.tools import list_ports
import serial
import struct
import time
import unittest
import math



customtkinter.set_default_color_theme("blue")

class Compass(customtkinter.CTkCanvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#585858", bd=0, highlightthickness=0)  # Supprimer le cadre blanc
        self.angle = 0
        self.second_angle = 90  # Initialise la deuxième flèche à 90°
        self.draw_compass()

    def draw_compass(self):
        self.delete("all")

        # Créer un cercle entourant la boussole avec un rayon légèrement plus petit
        self.create_oval(15, 15, 185, 185, fill="#585858", outline="black", width=2)

        # Ajout d'un cercle central pour la boussole
        self.create_oval(95, 95, 105, 105, fill="black")

        # Dessiner les deux flèches séparément
        self.arrow1 = self.draw_arrow(self.angle, "blue")
        self.arrow2 = self.draw_arrow(self.second_angle, "green")

        # Ajout des marques de direction N, S, E, W en dehors du cercle avec des coordonnées ajustées
        self.create_text(100, 5, text="N", font=("Helvetica", 14, "bold"), fill="darkred")
        self.create_text(100, 195, text="S", font=("Helvetica", 14, "bold"), fill="darkred")
        self.create_text(5, 100, text="W", font=("Helvetica", 14, "bold"), fill="darkred")
        self.create_text(195, 100, text="E", font=("Helvetica", 14, "bold"), fill="darkred")

    def draw_arrow(self, angle, color):
        rad_angle = math.radians(angle)
        x = 100 + 85 * math.sin(rad_angle)  # Ajustement du rayon pour correspondre au cercle réduit
        y = 100 - 85 * math.cos(rad_angle)  # Ajustement du rayon pour correspondre au cercle réduit
        return self.create_line(100, 100, x, y, fill=color, width=4, arrow=customtkinter.LAST, arrowshape=(18, 24, 8), smooth=True)

    def update_angle(self, angle):
        self.angle = angle
        self.delete(self.arrow1)
        self.arrow1 = self.draw_arrow(self.angle, "blue")

    def update_cap(self, angle):
        self.second_angle = angle
        self.delete(self.arrow2)
        self.arrow2 = self.draw_arrow(self.second_angle, "green")
                                      
class App(customtkinter.CTk):

    APP_NAME = "Batonome GUI"
    WIDTH = 800
    HEIGHT = 500



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        #Liste les ports COm disponible :
        self.port_tuple = ()
        self.listPortName = []
        self.listPortInit()
        self.com = "COM?"
        self.xbee = None
        
        self.timer=None
        self.countLine = "1.0"
        self.latitude = 0
        self.longitude = 0
        self.angle = 0
        self.sizeDataToreceive = 32
        self.firstDataReceived = False
        self.synchroRequest = False
        self.comandSerial = 1
        self.sensDerive = 5
        self.forceDerive = 5
        self.sensTirant = 5
        self.forceTirant = 5
        self.countUpdatePosition = 0
        self.valAngle = 10
        self.lastDataReceived=0

        
        
        #Tableau de 3 booleen pour savoir si le bateau est connecté
        self.boatConnected = [False,False,False]
            
        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/Icons")
        self.gps_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "GPS.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "GPS.png")), size=(20, 20))
        self.navigation_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "navigation.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "navigation.png")), size=(20, 20))

        self.disconnected_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "disconnected.png"))
                                                        , dark_image=Image.open(os.path.join(image_path, "disconnected.png")), size=(30, 30))

        self.connected_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "connected.png"))
                                                        , dark_image=Image.open(os.path.join(image_path, "connected.png")), size=(30, 30))

        self.marker_list = []
        self.marker_list_nav = []
        #InitZone
        self.initZoneValue = False
        self.listeGpsPoints = []
        self.baliseState = False
        self.baliseGPSCordinate = (0,0)
        self.nbGPSCoord = b'0'

        # ============ create two CTkFrames ============

        # self.grid_columnconfigure(0, weight=0)
        # self.grid_columnconfigure(1, weight=0)
        # self.grid_columnconfigure(2, weight=0)
        # self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)



        #Create the header frame
        self.frame_header = customtkinter.CTkFrame(master=self, height=50, corner_radius=0,fg_color="#2b2b2b")
        self.frame_header.grid(row=0, column=0,columnspan=2, padx=0, pady=0, sticky="nsew")

       
        

        #Create the log frame
        self.frame_log = customtkinter.CTkFrame(master=self, height=50, corner_radius=0, fg_color=None)
        self.frame_log.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")
        self.frame_log.grid_columnconfigure(0, weight=1)
       # self.frame_log.rowconfigure(0, weight=1)


        # Create the App frame
        self.frame_app = customtkinter.CTkFrame(master=self,  corner_radius=0,fg_color=None)
        self.frame_app.grid(row=2, column=0, padx=0, pady=0,sticky="nsew")
        self.frame_app.grid_columnconfigure(0, weight=0)
        self.frame_app.grid_columnconfigure(1, weight=1)
        self.frame_app.grid_rowconfigure(0, weight=1)


        #Create the nav_frame
        self.frame_nav = customtkinter.CTkFrame(master=self.frame_app, width=100, corner_radius=0, fg_color=None)
        self.frame_nav.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        

        #Create the seting_frame
        self.frame_setting = customtkinter.CTkFrame(master=self.frame_app, width = App.WIDTH, corner_radius=0)
        self.frame_setting.grid_columnconfigure(0, weight=0)
        self.frame_setting.grid_columnconfigure(1, weight=1)
        self.frame_setting.grid_rowconfigure(0, weight=1)

        self.frame_setting.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

        # #create the navigation frame
        self.frame_navigation = customtkinter.CTkFrame(master=self.frame_app, corner_radius=0,fg_color = "#585858")
        self.frame_navigation.grid_columnconfigure(1, weight=1)
        self.frame_navigation.grid_rowconfigure(0, weight=1)

        
        #Create the left frame settings
        self.frame_left = customtkinter.CTkFrame(master=self.frame_setting, width=100, corner_radius=0,fg_color = "#585858")
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        #create the right frame settings
        self.frame_right = customtkinter.CTkFrame(master=self.frame_setting, width=1200, corner_radius=0,fg_color = "#585858")
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        #Create the left frame_navigation
        self.frame_left_navigation = customtkinter.CTkFrame(master=self.frame_navigation, width=100, corner_radius=0,fg_color = "#585858")
        self.frame_left_navigation.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        #create the right frame_navigation
        self.frame_right_navigation = customtkinter.CTkFrame(master=self.frame_navigation, width=1200, corner_radius=0,fg_color = "#585858")
        self.frame_right_navigation.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")


        # ============ header ============

        self.frame_header.grid_columnconfigure(1, weight=1)
        self.frame_header.grid_columnconfigure(0, weight=1)
        self.frame_header.grid_rowconfigure(0, weight=1)

        self.frame_header_left= customtkinter.CTkFrame(master=self.frame_header, corner_radius=0,height = 50 ,width = 400, fg_color=None)
        self.frame_header_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
        self.frame_header_right= customtkinter.CTkFrame(master=self.frame_header,  corner_radius=0,height = 50, fg_color=None)
        self.frame_header_right.grid(row=0, column=1, padx=0, pady=0, sticky="nse")

        
        self.button_navigation = customtkinter.CTkButton(self.frame_nav, corner_radius=0, height=40, border_spacing=10, text="Navigation", image = self.navigation_image,
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.navigation_button_event)
        self.button_navigation.grid(row=1, column=0, padx=0, pady=0, sticky="ew")
        self.button_navigation.configure()

        # #Ajout du bouton connect
        self.button_connect = customtkinter.CTkButton(self.frame_header_right,  height=30,width=60, text=None, image = self.disconnected_image,
                                                   fg_color="red", hover_color="#ff2700",
                                                    command=self.connect)
        #changer la couleur du bouton
        self.button_connect.grid(row=0, column=1, padx=(20, 20), pady=(10, 0),sticky="nse")
        

        self.button_COM = customtkinter.CTkOptionMenu(self.frame_header_right, values=self.listPortName,width=90, height=30, command=self.majPortCom)
        self.button_COM.grid(row=0, column=0, padx=(20, 20), pady=(10, 0),sticky="nse")
        # ============ log ============
        self.LogTextbox = customtkinter.CTkTextbox(master=self.frame_log, height=50,corner_radius=0,text_color="white", fg_color="black" ,state = "normal")
        self.LogTextbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.LogTextbox.insert("0.0", "Log...\n")  # insert at line 0 character 0
        self.LogTextbox.insert("2.0", "Lag...\n")  # insert at line 0 character 0
        self.LogTextbox.insert("3.0", "Lug...\n")  # insert at line 0 character 0


        #self.LogTextbox = self.LogTextbox.get("0.0", "end")  # get text from line 0 character 0 till the end

        # ============ frame_app ============

        # ============ frame_nav ============

        #Add Button settings
        self.button_settings = customtkinter.CTkButton(self.frame_nav, corner_radius=0, height=40, border_spacing=10, text="Settings",image = self.gps_image,
                                                    fg_color=("gray75", "gray25"),text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.settings_button_event)
        self.button_settings.grid(row=0, column=0, padx=0, pady=0, sticky="ew")

        #Add Button Navigation
        self.button_navigation = customtkinter.CTkButton(self.frame_nav, corner_radius=0, height=40, border_spacing=10, text="Navigation", image = self.navigation_image,
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.navigation_button_event)
        self.button_navigation.grid(row=1, column=0, padx=0, pady=0, sticky="ew")
        self.button_navigation.configure()
       
        

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(3, weight=1)
         #Ajouter une image dans le bouton

        
        self.imageLock = customtkinter.CTkImage(light_image=Image.open("C://Users//scant//Dev//Batonome//Batonome-GUI//media//lock.png"),
                                  dark_image=Image.open("C://Users//scant//Dev//Batonome//Batonome-GUI//media//lock.png"),
                                  size=(20, 20))

        self.imageUnLock = customtkinter.CTkImage(light_image=Image.open("C://Users//scant//Dev//Batonome//Batonome-GUI//media//unlock.png"),
                                  dark_image=Image.open("C://Users//scant//Dev//Batonome//Batonome-GUI//media//unlock.png"),
                                  size=(20, 20))

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,text="Zone Nav",image=self.imageUnLock, command=self.initZone)
        self.button_1.grid(pady=(60, 0), padx=(20, 20), row=1, column=0)


        self.frameBaliseGPS = customtkinter.CTkFrame(master=self.frame_left, fg_color="transparent",width=150, corner_radius=0)
        self.frameBaliseGPS.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")
        self.frameBaliseGPS.grid_rowconfigure(1, weight=1)
        
        #Bouton pour mettre à jour la balise
        self.button_MajBalise = customtkinter.CTkButton(master=self.frameBaliseGPS,text="Balise",image = self.imageUnLock,command = self.baliseGPS)
        self.button_MajBalise.grid(pady=(30, 0), padx=(20, 20), row=0, column=0)

        #Zone de texte popur stocker les coordonnées GPS de la balise
        self.textBaliseLon = customtkinter.CTkTextbox(master=self.frameBaliseGPS, width=130, height=1)
        self.textBaliseLon.grid(pady=(5, 0), padx=(20, 20), row=1, column=0)

        #Zone de texte popur stocker les coordonnées GPS de la balise
        self.textBaliseLat = customtkinter.CTkTextbox(master=self.frameBaliseGPS, width=130, height=1)
        self.textBaliseLat.grid(row=3, column=0, padx=(20, 20), pady=(10, 0))



        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(pady=(5, 20), padx=(20, 20), row=3, column=0)
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"], command=self.change_map)
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

       # Bouton pour envoyer les infos au bateau
        self.button_SendBoat = customtkinter.CTkButton(master=self.frameBaliseGPS,text="Syncronisation", command = self.synchBatonome)
        self.button_SendBoat.grid(row=5, column=0, padx=(20, 20), pady=(10, 0))

        # Bouton pour envoyer les infos au bateau
        self.button_SendBoat = customtkinter.CTkButton(master=self.frameBaliseGPS,text="Calib Accelero", command = self.calibAccelero)
        self.button_SendBoat.grid(row=6, column=0, padx=(20, 20), pady=(10, 0))
        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        #Bouton calibration GPS
        self.button_6 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Calibration GPS",
                                                width=90, state="disabled",
                                                command=self.calibrationGPS)

        self.button_6.grid(row=0, column=2, sticky="w", padx=(12, 0), pady=12)


        self.map_widget.add_left_click_map_command(self.left_click_event)

        # Set default values
        #BERLIN
        self.map_widget.set_address("Paris")
        
        self.map_option_menu.set("Google satellite")
        self.button_COM.set("COM?")

        # ============ frame_left_navigation ============

        #Afficher la valeur de self.sensDerive dans frame_left_navigation avec un label :
        self.labelSensDerive = customtkinter.CTkLabel(self.frame_left_navigation, text="Sens de dérive : ", anchor="w")
        self.labelSensDerive.grid(pady=(5, 20), padx=(20, 20), row=0, column=0)

        #Afficher la valeur de self.powerDerive dans frame_left_navigation avec un label :
        self.labelPowerDerive = customtkinter.CTkLabel(self.frame_left_navigation, text="Puissance de dérive : ", anchor="w")
        self.labelPowerDerive.grid(pady=(5, 20), padx=(20, 20), row=1, column=0)

        #Afficher la valeur de self.sensTirant dans frame_left_navigation avec un label :
        self.labelSensTirant = customtkinter.CTkLabel(self.frame_left_navigation, text="Sens de tirant : ", anchor="w")
        self.labelSensTirant.grid(pady=(5, 20), padx=(20, 20), row=2, column=0)

        #Afficher la valeur de self.powerTirant dans frame_left_navigation avec un label :
        self.labelPowerTirant = customtkinter.CTkLabel(self.frame_left_navigation, text="Puissance de tirant : ", anchor="w")
        self.labelPowerTirant.grid(pady=(5, 20), padx=(20, 20), row=3, column=0)

        self.compass = Compass(self.frame_left_navigation, width=200, height=200)
        self.compass.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))
        


        
        # ============ frame_right_navigation ============

        # frame right navigation

        self.frame_right_navigation.grid_rowconfigure(0, weight=1)
        self.frame_right_navigation.grid_columnconfigure(0, weight=1)


        #Carte de navigation
        self.map_widget_navigation = TkinterMapView(self.frame_right_navigation, corner_radius=0)
        self.map_widget_navigation.grid(row=0, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        #Marker GPS Bateau
        self.markerBoat =  self.map_widget_navigation.set_marker( 48.858093, 2.294694, "Bato")


        
        #Gestion touche
        self.bind("<KeyPress>", self.key_up_pressed)
        

    def set_angle(self, angle):
        # Mettez à jour l'angle de la flèche
        self.coords(self.arrow, 150, 100, 145, 120, 155, 120, 150, 130)
        self.itemconfigure(self.arrow, fill="red")
        self.rotate(angle, 150, 150)

    def displaySensDerive(self, sensDerive):
        self.labelSensDerive.configure(text="Sens de dérive : " + str(sensDerive))

    def displaySensTirant(self, sensTirant):
        self.labelSensTirant.configure(text="Sens du tirant : " + str(sensTirant))

    def displayPowerDerive(self, powerDerive):
        self.labelPowerDerive.configure(text="Power de dérive : " + str(powerDerive))

    def displayPowerTirant(self, powerTirant):
        self.labelPowerTirant.configure(text="Power du tirant : " + str(powerTirant))

    
    def addLog(self, text):
        self.LogTextbox.insert(self.countLine, text+"\n")  # insert at line 0 character 0
        #self.countLine = self.countLine + 1
       # print(self.countLine)
        
    
    def settings_button_event(self):
        self.select_frame_by_name("settings")

    def navigation_button_event(self):
        self.select_frame_by_name("navigation")
        self.countUpdatePosition = 14
        self.setGPSOnMapNavigation(self.latitude,self.longitude)
    
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.button_settings.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")
        self.button_navigation.configure(fg_color=("gray75", "gray25") if name == "navigation" else "transparent")

        # show selected frame
        if name == "settings":
            self.frame_setting.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        else:
            self.frame_setting.grid_forget()
        if name == "navigation":
            self.frame_navigation.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

            #Set position on map with balise GPS
            #self.setGPSOnMapNavigation(float(self.textBaliseLat.get("0.0", "end")) , float(self.textBaliseLon.get("0.0", "end")))
           # print(float(self.textBaliseLat.get("0.0", "end")))
        else:
            self.frame_navigation.grid_forget()

    def update_compass(self,angle):
        self.compass.update_angle(angle)

    def update_cap(self,angle):
        self.compass.update_cap(angle)
        
    
    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    
        

    def setGPSOnMapNavigation(self, lat, lon):
        # set current widget position and zoom
        self.map_widget_navigation.set_position(lat, lon)  # Paris, France
        self.map_widget_navigation.set_zoom(18)

    def baliseGPS(self, event=None):
        if (self.baliseState==False):
            self.baliseState = True
            self.textBaliseLat.configure(state="disabled")
            self.textBaliseLon.configure(state="disabled")
            #Recupere les coordonnées GPS de la balise
            #self.baliseGPSCordinate = (float(self.textBaliseLat.get("0.0", "end")) , float(self.textBaliseLon.get("0.0", "end")))
            #Positionne une balise bleue
            #self.markerBaliseGPS = self.map_widget.set_marker(self.baliseGPSCordinate[0], self.baliseGPSCordinate[1])
            #Maj cadenas
            self.button_MajBalise.configure(image = self.imageLock)

        else:
            self.baliseState = False
            self.textBaliseLat.configure(state="normal")
            self.textBaliseLon.configure(state="normal")
            #Maj Cadena
            self.button_MajBalise.configure(image = self.imageUnLock)
            #Suprime la balise bleue
            self.markerBaliseGPS.delete()


    def left_click_event(self,coordinates_tuple):
        print(self.initZoneValue)
        print(self.baliseState)
        if (self.initZoneValue==False):
            #On vérifie que moins de 11 points ont été définis:
            if (len(self.listeGpsPoints) < 10):
                log = "Point GPS  "+str(len(self.listeGpsPoints)+1)+ "/10 :" +str(coordinates_tuple)
                self.addLog(log)
                self.marker_list.append(self.map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1]))
                self.listeGpsPoints.append(coordinates_tuple)
                print(self.listeGpsPoints)
            else:
                self.addLog("Vous avez défini 10 points, vous ne pouvez plus en ajouter")
        else:
            if (self.baliseState==False):
                #self.baliseGPS()
                self.markerBaliseGPS = self.map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1])
                self.baliseGPSCordinate = (float(coordinates_tuple[0]) , float(coordinates_tuple[1]))
                #Positionne les info GPS dans les textboxes
                self.textBaliseLat.delete("0.0", "end")
                self.textBaliseLon.delete("0.0", "end")
                self.textBaliseLat.insert("0.0", self.baliseGPSCordinate[0])
                self.textBaliseLon.insert("0.0", self.baliseGPSCordinate[1])
                self.baliseGPS()
                


    def initZone(self, event=None):
        if(self.initZoneValue == False):
            self.initZoneValue = True
            #Dessine le perimetre de navigation
            self.polygon_1 = self.map_widget.set_polygon(self.listeGpsPoints, fill_color=None,  outline_color="red",  border_width=12, name="Zone de navigation")
            #Affiche le cadenas lock sur le bouton
            self.button_1.configure(image=self.imageLock)

            #Si Nb de point GPS < 20, on comble la difference
            nbGPScoordToFill = len(self.listeGpsPoints)
            if (nbGPScoordToFill != 10):
                for i in range (nbGPScoordToFill,10):
                    self.listeGpsPoints.append((float(0),float(0)))

            print(self.listeGpsPoints)

        else:
            self.initZoneValue = False
            self.polygon_1.delete()
            self.listeGpsPoints.clear()
            self.button_1.configure(image=self.imageUnLock)
            self.clear_marker_event()

        

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def listPortInit(self):
        #Erase the tuple
        self.listPortName.clear()
        self.listPort = list_ports.comports()
        self.listPortName = []
        for port in self.listPort:
            self.listPortName.append(port.device)


    def connect(self):
        if(self.com == "COM?"):
            print("Veuillez selectionner un port COM valide")
            self.compass.update_angle(0+self.valAngle)
            self.compass.update_second_angle(90+self.valAngle)
            self.addLog("Veuillez selectionner un port COM valide")
            self.valAngle = self.valAngle + 10
        else:
            self.initCOM()
            print("Connexion au port COM : " + self.com)

            self.addLog("Connexion au port COM : " + self.com)
            self.addLog("Veuillez patienter...")
            self.addLog("")
            self.startThreadSerial()
            
    def startThreadSerial(self):
        #On emet toutes les secondes
        self.timer = threading.Timer(1.0, self.serialEmit)
        self.timer.start()
        #On lance le thread de reception
        self.thread = threading.Thread(target=self.serialThread)
        self.thread.start()

    def connectionLost(self):
        #On passe le bouton connect en orange
        self.button_connect.configure(fg_color="red",image = self.disconnected_image)
        pass

    def connectionEstablished(self):
        #On passe le bouton connect en bleu
        self.button_connect.configure(fg_color="#1f6aa5",image = self.connected_image)
       
        pass

    def serialThread(self):
        while True:
            #Si des data sont sur le port serie on affiche
            #I receive data from the serial port, data is a structure, i want to decode the data, the structure is composed by double, double, float, int
            
            received_data = bytearray()
        
            while len(received_data) < self.sizeDataToreceive:
                byte = self.xbee.read(1)
                
                if byte:
                    received_data.extend(byte)
                else:
                    break
        
        
            

            #si on a recu des données
            if received_data:

                if(self.firstDataReceived == False):
                    self.connectionEstablished()
                    self.firstDataReceived = True

                print(received_data)
                self.latitude = struct.unpack('d', received_data[0:8])[0]
                self.longitude = struct.unpack('d', received_data[8:16])[0]
                #first byte is the derivesDirection it's a char
                self.sensDerive = struct.unpack('B', received_data[16:17])[0]
                #next byte is the derivesDirection it's a char
                self.forceDerive = struct.unpack('B', received_data[17:18])[0]
                #first byte is the derivesDirection it's a char
                self.sensTirant = struct.unpack('B', received_data[18:19])[0]
                #next byte is the derivesDirection it's a char
                self.forceTirant = struct.unpack('B', received_data[19:20])[0]
                #first 2 bytes are the latitude it's a double
                #latitude = struct.unpack('d', received_data[4:12])[0]
                #next 2 bytes are the longitude it's a double
                #longitude = struct.unpack('d', received_data[12:20])[0]
                #next 4 bytes are the angle it's a float
                self.angle = struct.unpack('f', received_data[20:24])[0]
                self.cap = struct.unpack('f', received_data[24:28])[0]
                self.callibAccelero = struct.unpack('B', received_data[28:29])[0]

                self.displaySensDerive(self.sensDerive)
                self.displaySensTirant(self.sensTirant)
                self.displayPowerDerive(self.forceDerive)
                self.displayPowerTirant(self.forceTirant)
                self.update_cap(self.cap)
                print(self.callibAccelero)
                print(self.cap)

                #UPdate marker position boat
                #remove marker on map_widget_navigation
                #self.markerBoat.delete()
                #self.markerBoat =  self.map_widget_navigation.set_marker(self.latitude,self.longitude, "Bato")
                
                #self.map_widget_navigation.set_position(self.latitude, self.longitude)

                #self.map_widget_navigation.set_marker(self.map_widget_navigation, self.latitude, self.longitude)
                
                self.button_6.configure(state="enabled")
                #On met à jour la position du bateau toutes les 15 coups
                if(self.countUpdatePosition == 15):
                    self.map_widget_navigation.set_position(self.latitude, self.longitude)
                    self.markerBoat.delete()
                    self.markerBoat =  self.map_widget_navigation.set_marker(self.latitude,self.longitude, "Bato")
                    self.countUpdatePosition = 0
                else:
                    self.countUpdatePosition = self.countUpdatePosition + 1

                #MAJ angle du vent
                self.update_compass(self.angle)

                #Toutes les 5 secondes on met a jour la position du bateau
                


             
                print (self.latitude)
                print (self.longitude)
                print (self.angle)

            else:
               
                self.firstDataReceived = False
                print("Perte de connexion avec le bateau")
                self.addLog("Perte de connexion avec le bateau")
                self.connectionLost()
            


            if self.xbee.in_waiting > 0:
                data = self.xbee.readline().decode().rstrip()
                print(data)
                self.addLog(data)

    def calibrationGPS(self):
        self.addLog("Calibration GPS en cours...")
        self.map_widget.set_positionl:(self.latitude, self.longitude)
        self.map_widget.set_zoom(15)

    def calibAccelero(self):
        self.addLog("Calibration Accelero en cours...")
        self.comandSerial = 11 #send request accelerometer calibration

    
    def synchBatonome(self):
        self.comandSerial = 3
        self.addLog("Synchronisation avec le bateau en cours...")
        self.addLog("")
    
    
    
    def serialEmit(self):
        if self.comandSerial == 1:
            
            data = struct.pack('ccc',b'A',b'0',b'\n')
            self.xbee.write(data)
            print(data)
            print("send 4")

        elif self.comandSerial == 2:
            
            #Use pack to pack two char into variable dede
            print(struct.calcsize('cc'))
            dede = struct.pack('ccc',b'B',b'self.sizeReceiveGP',b'\n')
            self.xbee.write(dede)
            print("send 6")
            self.synchroRequest = True
            self.comandSerial = 3
            

        elif self.comandSerial == 3:
            #Aujourd'hui on doit envoyer 10 coordonnés GPS pour faire le tracé
            #data = struct.pack('ccddddddddddddddddddddddc',b'B', b'0',self.baliseGPSCordinate[0],self.baliseGPSCordinate[1],self.listeGpsPoints[0][0], self.listeGpsPoints[0][1],self.listeGpsPoints[1][0], self.listeGpsPoints[1][1], self.listeGpsPoints[2][0], self.listeGpsPoints[2][1], self.listeGpsPoints[3][0], self.listeGpsPoints[3][1], self.listeGpsPoints[4][0], self.listeGpsPoints[4][1],self.listeGpsPoints[5][0], self.listeGpsPoints[5][1], self.listeGpsPoints[6][0], self.listeGpsPoints[6][1], self.listeGpsPoints[7][0], self.listeGpsPoints[7][1],self.listeGpsPoints[8][0], self.listeGpsPoints[8][1],self.listeGpsPoints[9][0], self.listeGpsPoints[9][1], b'\n')
            data = struct.pack('ccddc',b'B', b'0',self.baliseGPSCordinate[0],self.baliseGPSCordinate[1], b'\n')

            # dddddddddddddddddddd   self.listeGpsPoints[5][0], self.listeGpsPoints[5][1], self.listeGpsPoints[6][0], self.listeGpsPoints[6][1], self.listeGpsPoints[7][0], self.listeGpsPoints[7][1],self.listeGpsPoints[8][0], self.listeGpsPoints[8][1],self.listeGpsPoints[9][0], self.listeGpsPoints[9][1],b'\n')
            print(str(type(data)))
            print(str(len(data)))
            print(self.listeGpsPoints)
            self.xbee.write(data)
            self.addLog("Configuration envoyée au bateau")
            # if (data.find('\n') < 2):
            #     self.xbee.write(data)
            #     self.addLog("Configuration envoyée au bateau")
            # else : 
            #     self.addLog("Erreur de transmission des données, retour chariot dans la trame")
            print(data)
            self.comandSerial = 1
        
        elif self.comandSerial == 4: #Touche RIGHT
            data = struct.pack('ccc',b'C',b'0',b'\n')
            self.xbee.write(data)
            print(data)
            self.comandSerial = 1

        elif self.comandSerial == 5: #Touche LEFT
            data = struct.pack('ccc',b'C',b'1',b'\n')
            self.xbee.write(data)
            print(data)
            self.comandSerial = 1

        
        
        elif self.comandSerial == 6: #Touche UP
            data = struct.pack('ccc',b'D',b'0',b'\n')
            self.xbee.write(data)
            print(data)
            self.comandSerial = 1

        elif self.comandSerial == 7: #Touche DOWN
            data = struct.pack('ccc',b'D',b'1',b'\n')
            self.xbee.write(data)
            print(data)
            self.comandSerial = 1

        elif self.comandSerial == 8: #Touche SPACE
            data = struct.pack('ccc',b'C',b'2',b'\n')
            self.xbee.write(data)
            print(data)
            self.comandSerial = 1

        elif self.comandSerial == 9: #Touche ENTER
            data = struct.pack('ccc',b'D',b'2',b'\n')
            self.xbee.write(data)
            print(data)
            self.comandSerial = 1

        elif self.comandSerial == 10: #Touche ENTER
            data = struct.pack('ccc',b'E',b'0',b'\n')
            self.xbee.write(data)
            print(data)
            self.comandSerial = 1

        elif self.comandSerial == 11: #CALIB ACCELERO
            data = struct.pack('ccc',b'F',b'0',b'\n')
            self.xbee.write(data)
            print(data)
            self.comandSerial = 1

            
            
        self.timer = threading.Timer(1.0, self.serialEmit)
        self.timer.start()
    
    def majPortCom(self,new_com: str):
        self.com = new_com
        self.addLog("Port COM selectionné : ")
        print(self.com)


    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def initCOM(self):
        # Ouvre la liaison série sur le port sélectionné à une vitesse de 9600 bauds
        self.xbee = serial.Serial(self.com, 9600,timeout=5)
    
    

    def on_closing(self, event=0):
        self.destroy()
        #Ferme les threads
        self.timer.cancel()
   
        #Bug si on clos le thread timer avant de fermer la fenêtre
        self.timer.cancel()

    def start(self):
        self.mainloop()

    def key_up_pressed(self,event):
        #On gère les touche seulement si on est dans la frame navigation
        if self.frame_right_navigation.winfo_ismapped():
            if event.keysym == "Up":
                print("Key up pressed")
                self.comandSerial = 6
            elif event.keysym == "Down":
                print("Key Down pressed")
                self.comandSerial = 7
            elif event.keysym == "Left":
                print("Key Left pressed")
                self.comandSerial = 5
            elif event.keysym == "Right":
                print("Key Right pressed")
                self.comandSerial = 4
            elif event.keysym == "space":
                print("Space Right pressed")
                self.comandSerial = 8
            elif event.keysym == "Return":
                print("Space Right pressed")
                self.comandSerial = 9
            elif event.keysym == "t":
                print("t Right pressed")
                self.comandSerial = 10
            


def thread1():
    t1 = threading.Thread(target=serie)
    t1.start()

def thread2():
    t2 = threading.Thread(target=graphic)
    t2.start()

def serie():
    print("Thread 1")



def graphic():
    pass
    



if __name__ == "__main__":
    app = App()
    app.start()

