'''
Description: This file contains the class to create the homepage for the simulation tool
Author: Andrew Lucentini :-)
'''
import tkinter as tk
from MainView import MainView
from MechanicalWorkshop.MWController import MechanicalWorkshopController
from Thermocouple.TCController import ThermocoupleController
"""
The main simulation controller
"""
class MainController(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Materials Lab Simulation Tool")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initialize Mechanical workshop page
        self.Page1 = MechanicalWorkshopController(container, self)
        self.Page1.page1.grid(row=0, column=0, sticky="nsew")
        self.Page1.page2.grid(row=0, column=0, sticky="nsew")

        # Initialize thermocouple page
        self.Page2 = ThermocoupleController(container, self)
        self.Page2.page1.grid(row=0, column=0, sticky="nsew")

        # Initialize main view
        self.HomePage = MainView(container, self)
        self.HomePage.grid(row=0, column=0, sticky="nsew")

        # Bind buttons to show_frame
        self.HomePage.pages[0].configure(command = lambda: self.show_frame(0))
        self.HomePage.pages[1].configure(command = lambda: self.show_frame(1))
        self.HomePage.tkraise()

    def show_frame(self, page):
        """
        Show a given page
        """
        if page == 0:
            self.Page1.page1.tkraise()
        else:
            self.Page2.page1.tkraise()

    def mainPage(self):
        """
        Function to raise the home page
        """
        self.HomePage.tkraise()