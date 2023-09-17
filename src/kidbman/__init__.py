from tkinter.filedialog import askopenfilename

import re

from kidbman.database_reader import LibraryDatabase
from kidbman.libdb_reader import DatabaseDescription, Library, Field

def synchronise(filepath):
    # Create a connection to the library and use this to link in to the database.
    kicad_dbl = DatabaseDescription.from_filepath(filepath)
    database = LibraryDatabase.from_source(kicad_dbl['source'])

    # get all the tables and get all the fields, craete a list of them.
    libraries = []
    for table_name in database.get_table_names():
        new_library: Library = None

        # Bin the temp ones.
        if re.match(r'~TMPCLP.*', table_name):
            continue
        if table_name in kicad_dbl.get_library_names():
            new_library: Library = kicad_dbl.get_library(table_name)
        else:
            new_library = Library(
                name=table_name,
                table=table_name,
                key="Part Number",
                symbols="Symbols",
                footprints="Footprints",
                fields=[]
            )
        # look through the fields, if anything isn't there, add in the default values.
        for field_name in database.get_table_fields(table_name):
            if field_name not in new_library.get_field_names():
                new_field = Field(
                    column=field_name,
                    name=field_name,
                    visible_on_add=False,
                    visible_in_chooser=True,
                    show_name=True,
                    inherit_properties=True
                )
                new_library.fields.append(new_field)
        # [new_library.delete_field(delete_field) for delete_field in new_library.get_field_names() if delete_field not in database.get_table_fields(new_library.table)]
        libraries.append(new_library)

    kicad_dbl["libraries"] = libraries
    kicad_dbl.save(filepath)