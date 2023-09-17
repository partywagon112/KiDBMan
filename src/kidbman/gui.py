from typing import Any
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from kidbman.database_reader import LibraryDatabase
from kidbman.libdb_reader import DatabaseDescription

from tkinter.filedialog import askopenfilename, asksaveasfilename

from abc import ABCMeta, abstractmethod, abstractclassmethod

class Dashboard(ttk.Window):
    """
    Basic dashboard interface for the application.
    """
    def __init__(self, filepath = None, title="KiCAD DBLib Man", themename="superhero", iconphoto='', size=None, position=None, minsize=None, maxsize=None, resizable=None, hdpi=True, scaling=None, transient=None, overrideredirect=False, alpha=1):
        super().__init__(title, themename, iconphoto, size, position, minsize, maxsize, resizable, hdpi, scaling, transient, overrideredirect, alpha)        
        self.filepath = filepath
        self.metadata:DatabaseDescription = DatabaseDescription(filepath)

        self.mainleftframe = ttk.Frame(master=self)

        self.load_button = ttk.Button(master=self.mainleftframe, text='Load', command=self.load)
        self.load_button.pack(fill=BOTH, padx=10, pady=5)

        self.database_config:DatabaseMetaFrame = DatabaseMetaFrame.from_metadata(master=self.mainleftframe, meta=self.metadata, padding=10)
        self.database_config.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.odbc_config:ConfigureSourceFrame = ConfigureSourceFrame.from_metadata(master=self.mainleftframe, meta=self.metadata, padding=10)
        self.odbc_config.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.connect_button = ttk.Button(master=self.mainleftframe, text='Save and Connect', command=self.connect)
        self.connect_button.pack(fill=BOTH, padx=10, pady=5)

        self.connected_label = ttk.Label(master=self.mainleftframe, text="Not Connected")
        self.connected_label.pack(fill=BOTH, padx=10, pady=2)          

        self.save_button = ttk.Button(master=self.mainleftframe, text='Save As', command=self.save_meta_as)
        self.save_button.pack(padx=10, pady=5, anchor='sw', fill='both')

        self.mainleftframe.pack(anchor='w')

        # self.mainrightframe = ttk.Frame(master=self)
        # self.libraryframe = LibrariesManager()

    def connect(self):
        self.update_meta()
        self.metadata.save(self.filepath)
        try:
            self.connection = self.odbc_config.connect()
            self.connected_label.configure(text="Connected", bootstyle="success")
        except Exception as exception:
            print(exception)
            self.connected_label.configure(text="Failed!", bootstyle="danger")
    
    def load(self):
        self.filepath = askopenfilename(filetypes=[("KiCAD Database Library", "*.kicad_dbl")])
        self.metadata:DatabaseDescription = DatabaseDescription(self.filepath)
        
        self.database_config.set_from_metadata(self.metadata)
        self.odbc_config.set_from_metadata(self.metadata)

        self.connect()

    def update_meta(self):
        """
        Updates all the metadata frames to match what is relevant.
        """
        self.metadata.update(self.database_config.get())
        self.metadata['source'].update(self.odbc_config.get())

    def save_meta(self):
        self.update_meta()
        self.metadata.save(self.filepath)
    
    def save_meta_as(self):
        filepath = asksaveasfilename(filetypes=[("KiCAD Database Library", "*.kicad_dbl")])
        if filepath == "":
            return 
        self.filepath = filepath
        self.save_meta()

class GetableConfigFrame(metaclass=ABCMeta):
    @abstractclassmethod
    def from_metadata(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def set(self):
        pass

    @abstractmethod
    def set_from_metadata(self):
        pass


class FieldEntryFrame(ttk.Frame):
    def __init__(self, master, field, value, type:type = str, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.field = field
        self.entry = value
        self.type = type

        ttk.Label(master=self, text=field, width=20).pack(side='left', anchor='e')

        self.entry_box = ttk.Entry(self, validate='focus')
        self.entry_box.pack(padx=5, pady=5, anchor='w', expand=True, side="right", fill='x')

        self.set(value)
    
    def set(self, value):
        # self.entry_box.delete(first=ttk.FIRST, last=ttk.END)
        self.entry_box.insert(0, value)

    def get(self):
        return self.type(self.entry_box.get())

class DatabaseMetaFrame(ttk.Labelframe, GetableConfigFrame):
    """
    Frame for basic database details.
    """
    def __init__(self, master, version: dict, name, description, *args, **kwargs):
        super().__init__(text="Metadata", master=master, *args, **kwargs)
        self.name = FieldEntryFrame(master=self, field='Name', value=name)
        self.name.pack(padx=5, pady=5, anchor='w', expand=True, fill='both')
        self.description = FieldEntryFrame(master=self, field='Description', value=description)
        self.description.pack(padx=5, pady=5, anchor='w', expand=True, fill='both')
        self.version = FieldEntryFrame(master=self, field='Version', value=version)
        self.version.pack(padx=5, pady=5, anchor='w', expand=True, fill='both')
    
    def set(self, version: str = None, name: str = None, description: str = None):
        self.version.set(version) if version != None else None
        self.name.set(name) if name != None else None
        self.description.set(description) if description != None else None
    
    def set_from_metadata(self, meta: dict):
        self.version.set(meta['meta']['version'] if 'version' in meta['meta'].keys() else 0 if 'meta' in meta.keys() else 0)
        self.name.set(meta['name'] if 'name' in meta.keys() else "UNKNOWN")
        self.description.set(meta['description'] if 'description' in meta.keys() else "")

    def get(self):
        """
        Use this to update these fields of the meta.
        """
        return {
            'meta': {
                'version': self.version.get()
            },
            'name': self.name.get(),
            'description': self.description.get()
        }

    @classmethod
    def from_metadata(cls, master, meta: dict, *args, **kwargs):
        version = meta['meta']['version'] if 'version' in meta['meta'].keys() else 0 if 'meta' in meta.keys() else 0
        name = meta['name'] if 'name' in meta.keys() else "UNKNOWN"
        description = meta['description'] if 'description' in meta.keys() else ""
        return cls(master, version, name, description, *args, **kwargs)

class ConfigureSourceFrame(ttk.Labelframe, GetableConfigFrame):
    """
    Basic configuration window for the source configuration.
    """
    def __init__(self, master, type: str = "", dsn: str = "", username: str = "", password: str = "", timeout_seconds: int = 2, connection_string: str = "", *args, **kwargs):
        super().__init__(master=master, text="Source Configuration", *args, **kwargs)
        self.type = FieldEntryFrame(self, "Type", type)
        self.dsn = FieldEntryFrame(self, "DSN", dsn)
        self.username = FieldEntryFrame(self, "Username", username)
        self.password = FieldEntryFrame(self, "Password", password)
        self.timeout_seconds = FieldEntryFrame(self, "Timeout Seconds", timeout_seconds, type=int)
        self.connection_string = FieldEntryFrame(self, "Connection String", connection_string)

        self.type.pack(padx=5, pady=5, anchor='w', expand=True, fill="both")
        self.dsn.pack(padx=5, pady=5, anchor='w', expand=True, fill="both")
        self.username.pack(padx=5, pady=5, anchor='w', expand=True, fill="both")
        self.password.pack(padx=5, pady=5, anchor='w', expand=True, fill="both")
        self.timeout_seconds.pack(padx=5, pady=5, anchor='w', expand=True, fill="both")
        self.connection_string.pack(padx=5, pady=5, anchor='w', expand=True, fill="both")
    
    @classmethod
    def from_metadata(cls, master, meta: dict, *args, **kwargs):
        if 'source' not in meta.keys():
            source = {
                'type': '',
                'dsn': '',
                'username': '',
                'password': '',
                'timeout_seconds': 2,
                'connection_string': ''
            }
        else:
            source = meta['source']

        return cls(
            master=master,
            type = source['type'],
            dsn = source['dsn'],
            username = source['username'],
            password = source['password'],
            timeout_seconds = source['timeout_seconds'],
            connection_string = source['connection_string'],
            *args,
            **kwargs
        )
    
    def connect(self):
        """
        Retreives the current configuration and attempts to bond to the SQL server.
        """
        return LibraryDatabase.from_source(self.get())

    def get(self):
        return {
            'type': self.type.get(),
            'dsn': self.dsn.get(),
            'username': self.username.get(),
            'password': self.password.get(),
            'timeout_seconds': self.timeout_seconds.get(),
            'connection_string': self.connection_string.get()
        }

    def set(self, type: str = None, dsn: str = None, username: str = None, password: str = None, timeout_seconds: int = None, connection_string: str = None):
        self.type.set(type) if type != None else None
        self.dsn.set(dsn) if dsn != None else None
        self.username.set(username) if username != None else None
        self.password.set(password) if password != None else None
        self.timeout_seconds.set(timeout_seconds) if timeout_seconds != None else None
        self.connection_string.set(connection_string) if connection_string != None else None

    def set_from_metadata(self, meta: dict, *args, **kwargs):
        self.type.set(meta['source']['type'] if 'type' in meta['source'].keys() else "")
        self.dsn.set(meta['source']['dsn'] if 'dsn' in meta['source'].keys() else "")
        self.username.set(meta['source']['username'] if 'username' in meta['source'].keys() else "")
        self.password.set(meta['source']['password'] if 'password' in meta['source'].keys() else "")
        self.timeout_seconds.set(int(meta['source']['timeout_seconds']) if 'timeout_seconds' in meta['source'].keys() else 2)
        self.connection_string.set(meta['source']['connection_string'] if 'connection_string' in meta['source'] else "")
