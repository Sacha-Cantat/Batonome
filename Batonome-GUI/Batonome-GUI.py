import sys
import tkinter as tk
import tkinter.messagebox
from tkintermapview import TkinterMapView

class App(tkinter.Tk):

    APP_NAME = "map_view_demo.py"
    WIDTH = 800
    HEIGHT = 750

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        
        #Nom de l'application
        self.title(self.APP_NAME)
        #Taille de l'application
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        #InitZone
        self.initZoneValue = False
        self.listeGpsPoints = []

        #Fermeture de l'application
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        #Recherche
        #self.bind("<Return>", self.search)

        #Si le système d'exploitation est Mac OS
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)

        #Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(1, weight=1)

        #Barre de recherche
        self.search_bar = tk.Entry(self, width=50)
        self.search_bar.grid(row=0, column=0, pady=10, padx=10, sticky="we")
        self.search_bar.focus()

        #Bouton de recherche
        self.search_bar_button = tk.Button(master=self, width=8, text="Init Zone", command=self.initZone)
        self.search_bar_button.grid(row=0, column=1, pady=10, padx=10)

        #Barre de zoom
        self.zoom_bar = tk.Scale(self, from_=4, to=20, orient=tkinter.HORIZONTAL, command=self.zoom)
        self.zoom_bar.grid(row=0, column=2, pady=10, padx=10)

        self.map_view = TkinterMapView(width=self.WIDTH, height=600,corner_radius=0)
        self.map_view.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.map_view.set_position(48.860381, 2.338594)  # Paris, France
    
        self.map_view.add_left_click_map_command(self.left_click_event)
    

    def left_click_event(self,coordinates_tuple):
        print(self.initZoneValue)
        
        if self.initZoneValue:
            print("Left click event with coordinates:", coordinates_tuple)
            self.map_view.set_marker(coordinates_tuple[0], coordinates_tuple[1])
            self.listeGpsPoints.append(coordinates_tuple)
            print(self.listeGpsPoints)
    

    


    
    def initZone(self, event=None):
        self.initZoneValue = True

    def zoom(self, event=None):
        pass

    def on_closing(self, event=0):
        self.destroy()
        exit()

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()        