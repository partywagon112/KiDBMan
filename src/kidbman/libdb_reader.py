import json





class Field():
    def __init__(self, column: str, name: str = "", visible_on_add: bool = False, visible_in_chooser: bool = True, show_name: bool = False, inherit_properties: bool = True):
        self.column = column
        self.name = name if name != "" else column
        self.visible_on_add = visible_on_add
        self.visible_in_chooser = visible_in_chooser
        self.show_name = show_name
        self.inherit_properties = inherit_properties
    
    def __setitem__(self, key, item):
        setattr(self, key, item)
    
    def __getitem__(self, item):
        return getattr(self, str(item))

    def __str__(self):
        return str(self.to_dict())

    @classmethod
    def from_dict(cls, kwargs):
        return cls(**kwargs)
    
    def to_dict(self) -> dict:
        return vars(self)


class Properties(Field):
    def __init__(self, description: str = "Description", footprint_filters: str = "Footprint Filters", keywords: str = "Keywords", exclude_from_bom: str = "No BOM", exclude_from_board: str = "Schematic Only"):
        self.description = description
        self.footprint_filters = footprint_filters
        self.keywords = keywords
        self.exclude_from_bom = exclude_from_bom
        self.exclude_from_board = exclude_from_board


class Library():
    def __init__(self, name, table, key: str = "Part ID", symbols: str = "Symbols", footprints: str = "Footprints", fields: list[Field] = [], properties: Properties = Properties()):
        self.name = name
        self.table = table
        self.key = key
        self.symbols = symbols
        self.footprints = footprints
        self.fields = fields
        self.properties = properties
    
    def __str__(self):
        return str(self.to_dict())

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, item):
        setattr(self, key, item)
    
    def set_field_value(self, field, key, value):
        """
        Provides direct access to the data source. Not recommended.
        """
        new_field = self.get_field(field)
        new_field[key] = value
        self.set_field(new_field)
    
    def to_dict(self) -> dict:
        library_dict = vars(self)
        library_dict['fields'] = [field.to_dict() for field in library_dict['fields']]
        library_dict['properties'] = library_dict['properties'].to_dict()
        return library_dict

    def get_field_names(self):
        return [field['name'] for field in self.fields]

    def get_field(self, name):
        return [field for field in self.fields if field.name == name][0]

    def set_field(self, field: Field):
        if field.name in  self.get_field_names():
            self.delete_field(field.name)
        self.fields.append(field.to_dict())

    def delete_field(self, name):
        self.fields.remove(self.get_field(name).to_dict())

    @classmethod
    def from_dict(cls, kwargs):
        return cls(**kwargs)

    def get_fields(self, *args, **kwargs) -> list[Field]:
        return [Field(field) for field in self.fields]

class DatabaseDescription(dict):
    def __init__(self, filepath, *args, **kwargs):
        self.filepath = filepath
        super().update(read_Database(self.filepath))

    def configure_source(self, type, dsn, username, password, timeout_seconds, connection_string):
        self["source"] = {
            "time": type,
            "dsn": dsn,
            "username": username,
            "password": password,
            "timeout_seconds": timeout_seconds,
            "connection_string": connection_string
        }
    
    def set_library_field_value(self, library, field, key, value):
        """
        Provides direct access to the data source. Not recommended.
        """
        new_library = self.get_library(library)
        new_library.set_field_value(field, key, value)
        self.set_library(new_library)

    def set_library(self, library: Library):
        if library.name in self.get_library_names():
            # if yo got a problem yea i'll solve it, check out the mic while the dj revolve it.
            # DELETING LIBRARY!!!!
            self.delete_library(library.name)
        self["libraries"].append(library.to_dict())

    def delete_library(self, name):
        self["libraries"].remove(self.get_library(name).to_dict())

    def get_library(self, name) -> Library:
        # get the index first
        return [Library.from_dict(library) for library in self["libraries"] if library['name'] == name][0]

    def get_library_names(self):
        """
        Returns easy lookup of libraries.
        """
        return [library['name'] for library in self["libraries"]]

    # @classmethod
    # def load(cls, filepath):
    #     cls(filepath)
    #     cls = read_Database(filepath)
    #     return cls

    def save(self, filepath: str = None):
        self.filepath = filepath if filepath != None else self.filepath
        self['libraries'] = [library.to_dict() if type(library) == Library else library for library in self['libraries']] 
        save_Database(self, self.filepath)

def read_Database(filepath: str) -> dict:
    with open(filepath) as Database_file:
        return json.load(Database_file)

def save_Database(Database, filepath: str):
    with open(filepath, 'w') as Database_file:
        json.dump(Database, Database_file, indent=4)

