import customtkinter
import PIL
from tkintermapview import TkinterMapView
from PIL import Image,ImageTk

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

        self.marker_list = []
        #InitZone
        self.initZoneValue = False
        self.listeGpsPoints = []
        self.baliseState = False

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

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
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)
       

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,text="Clear Markers",command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)


        self.frameBaliseGPS = customtkinter.CTkFrame(master=self.frame_left, width=150, corner_radius=0, fg_color=None)
        self.frameBaliseGPS.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")
        self.frameBaliseGPS.grid_rowconfigure(2, weight=1)
        
        #Bouton pour mettre à jour la balise
        self.button_MajBalise = customtkinter.CTkButton(master=self.frameBaliseGPS,text="Balise",command = self.baliseGPS)
        self.button_MajBalise.grid(pady=(30, 0), padx=(20, 20), row=0, column=0)

        #Zone de texte popur stocker les coordonnées GPS de la balise
        self.textBaliseLon = customtkinter.CTkTextbox(master=self.frameBaliseGPS, width=130, height=1)
        self.textBaliseLon.grid(pady=(5, 0), padx=(20, 20), row=1, column=0)

        #Zone de texte popur stocker les coordonnées GPS de la balise
        self.textBaliseLat = customtkinter.CTkTextbox(master=self.frameBaliseGPS, width=130, height=1)
        self.textBaliseLat.grid(pady=(5, 20), padx=(20, 20), row=2, column=0)



        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=4, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"], command=self.change_map)
        self.map_option_menu.grid(row=5, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=(20, 20), pady=(10, 20))

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

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def baliseGPS(self, event=None):
        if (self.baliseState==False):
            self.baliseState = True
            self.textBaliseLat.configure(state="disabled")
            self.textBaliseLon.configure(state="disabled")
        else:
            self.baliseState = False
            self.textBaliseLat.configure(state="normal")
            self.textBaliseLon.configure(state="normal")

    def left_click_event(self,coordinates_tuple):
        print(self.initZoneValue)
        print(self.baliseState)
        if (self.initZoneValue==False):
            print("Left click event with coordinates:", coordinates_tuple)
            self.marker_list.append(self.map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1]))
            self.listeGpsPoints.append(coordinates_tuple)
            print(self.listeGpsPoints)


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
