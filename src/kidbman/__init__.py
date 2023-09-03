from kidbman import gui, libdb_reader
import tkinter
from tkinter.filedialog import askopenfilename

class App():
    def __init__(self, filename: str = None):
        if filename == None:
            self.filename = askopenfilename(filetypes=[("KiCAD Database Library", "*.kicad_dbl")])

        self.lib_meta = libdb_reader.DatabaseDescription.load(self.filename)
        
    def start_dashboard(self):
        self.dashboard = gui.Dashboard(self.lib_meta)
        self.dashboard.mainloop()