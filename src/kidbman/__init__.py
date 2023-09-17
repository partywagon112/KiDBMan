from kidbman import gui
from tkinter.filedialog import askopenfilename

class App():
    def __init__(self, filename: str = None):
        if filename == None:
            self.filename = askopenfilename(filetypes=[("KiCAD Database Library", "*.kicad_dbl")])

    def start_dashboard(self):
        self.dashboard = gui.Dashboard(self.filename)
        self.dashboard.mainloop()