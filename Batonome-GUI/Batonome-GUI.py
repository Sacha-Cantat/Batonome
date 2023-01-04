import customtkinter
import PIL
from tkintermapview import TkinterMapView
from PIL import Image,ImageTk
import os

customtkinter.set_default_color_theme("blue")


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
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/Icons")
        self.gps_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "GPS.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "GPS.png")), size=(20, 20))
        self.navigation_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "navigation.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "navigation.png")), size=(20, 20))

        self.marker_list = []
        #InitZone
        self.initZoneValue = False
        self.listeGpsPoints = []
        self.baliseState = False
        self.baliseGPSCordinate = (0,0)

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
        self.frame_header = customtkinter.CTkFrame(master=self, height=50, corner_radius=0, fg_color=None)
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

        # ============ header ============

        # ============ log ============
        self.LogTextbox = customtkinter.CTkTextbox(master=self.frame_log, height=50,corner_radius=0,text_color="white", fg_color="black" ,state = "normal")
        self.LogTextbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.LogTextbox.insert("0.0", "Log...")  # insert at line 0 character 0
        self.LogTextbox = self.LogTextbox.get("0.0", "end")  # get text from line 0 character 0 till the end

        # ============ frame_app ============

        # ============ frame_nav ============

        #Add Button settings
        self.button_settings = customtkinter.CTkButton(self.frame_nav, corner_radius=0, height=40, border_spacing=10, text="Settings",image = self.gps_image,
                                                    fg_color="transparent",text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.settings_button_event)
        self.button_settings.grid(row=0, column=0, padx=0, pady=0, sticky="ew")

        #Add Button Navigation
        self.button_navigation = customtkinter.CTkButton(self.frame_nav, corner_radius=0, height=40, border_spacing=10, text="Navigation", image = self.navigation_image,
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.navigation_button_event)
        self.button_navigation.grid(row=1, column=0, padx=0, pady=0, sticky="ew")

       
        

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
        self.textBaliseLat.grid(pady=(5, 20), padx=(20, 20), row=2, column=0)



        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"], command=self.change_map)
        self.map_option_menu.grid(row=6, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=(20, 20), pady=(10, 20))

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

        self.map_widget.add_left_click_map_command(self.left_click_event)

        # Set default values
        self.map_widget.set_address("Berlin")
        self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")
    
    def settings_button_event(self):
        self.select_frame_by_name("settings")

    def navigation_button_event(self):
        self.select_frame_by_name("navigation")
    
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
        else:
            self.frame_navigation.grid_forget()

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

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
            print("Left click event with coordinates:", coordinates_tuple)
            self.marker_list.append(self.map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1]))
            self.listeGpsPoints.append(coordinates_tuple)
            print(self.listeGpsPoints)
        else:
            if (self.baliseState==False):
                #self.baliseGPS()
                self.markerBaliseGPS = self.map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1])
                self.baliseGPSCordinate = (float(coordinates_tuple[0]) , float(coordinates_tuple[0]))
                #Positionne les info GPS dans les textboxes
                self.textBaliseLat.delete("0.0", "end")
                self.textBaliseLon.delete("0.0", "end")
                self.textBaliseLat.insert("0.0", self.baliseGPSCordinate[0])
                self.textBaliseLon.insert("0.0", self.baliseGPSCordinate[1])
                self.baliseGPS()
                


    def initZone(self, event=None):
        if(self.initZoneValue == False):
            self.initZoneValue = True
            self.polygon_1 = self.map_widget.set_polygon(self.listeGpsPoints, fill_color=None,  outline_color="red",  border_width=12, name="Zone de navigation")
            self.button_1.configure(image=self.imageLock)
        else:
            self.initZoneValue = False
            self.polygon_1.delete()
            self.listeGpsPoints.clear()
            self.button_1.configure(image=self.imageUnLock)
            self.clear_marker_event()

        

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    
    

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
