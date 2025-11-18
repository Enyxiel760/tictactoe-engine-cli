from src.controllers import AbstractController
from src import views
import tkinter as tk


class GUIController(AbstractController):

    def __init__(self):
        self.root = tk.Tk()
        self.view = views.GUIView(self.root)

    def run(self) -> None:
        if not self.setup_game():
            return  # Exit if setup failed. (e.g. bad config)
        self.root.mainloop()
