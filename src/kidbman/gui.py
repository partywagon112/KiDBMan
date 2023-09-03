from typing import Any
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Dashboard(ttk.Window):
    """
    Basic dashboard interface for the application.
    """
    def __init__(self, metadata, title="KiCAD DBLib Man", themename="superhero", iconphoto='', size=None, position=None, minsize=None, maxsize=None, resizable=None, hdpi=True, scaling=None, transient=None, overrideredirect=False, alpha=1):
        super().__init__(title, themename, iconphoto, size, position, minsize, maxsize, resizable, hdpi, scaling, transient, overrideredirect, alpha)        
        self.metadata = metadata

        self.odbc_config = ConfigureODBCFrame(master=self, source=self.metadata['source'], padding=10)
        self.odbc_config.pack(fill=BOTH, expand=True, padx=10, pady=10)

class FieldEntryFrame(ttk.Frame):
    def __init__(self, field, entry, default_entry, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field = field
        self.entry = entry

        ttk.Label(master=self, text=field, width=20).pack(side='left', anchor='e', expand=True, fill=BOTH)

        self.entry_box = ttk.Entry(self, validate="focus", textvariable=ttk.Variable(master=self, value=entry))
        self.entry_box.pack(padx=5, pady=5, anchor='w', expand=True, side="right")

    def get(self):
        return self.entry_box.get()
    
    def set(self, value):
        self.entry_box.configure(textvariable=ttk.Variable(master=self, value=value))

class ConfigureODBCFrame(ttk.Labelframe):
    """
    Basic configuration window.
    """
    def __init__(self, source: dict, *args, **kwargs):
        super().__init__(text="Source Configuration", *args, **kwargs)
        # ttk.Label(master=self, text="Source Configuration").pack(anchor='center', side="top")
        
        self.boxes = {field: FieldEntryFrame(field.replace('_', ' ').title(), entry, "", master=self) for field, entry in source.items()}
        for box in self.boxes.values():
            box.pack(padx=5, pady=5, anchor='w', expand=True)

    def __getitem__(self, key: str) -> Any:
        return {self.boxes:  self.boxes.items()}
