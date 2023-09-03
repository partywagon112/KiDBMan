"""
This script is able to automatically update the description of a kicad_dblib file.

Need to create an intermediary object to hide some things away, but this works.
"""
from kidbman.database_reader import LibaryDatabase
from kidbman.libdb_reader import DatabaseDescription, Library, Field

KICAD_DBL_FILEPATH = "configuration.kicad_dbl"

# Create a connection to the library and use this to link in to the database.
kicad_dbl = DatabaseDescription(KICAD_DBL_FILEPATH)
database = LibaryDatabase.from_source(kicad_dbl['source'])

# get all the tables and get all the fields, craete a list of them.
libraries = []
for table_name in database.get_table_names():
    new_library: Library = None
    if table_name in kicad_dbl.get_library_names():
        new_library: Library = kicad_dbl.get_library()
    else:
        new_library = Library(
            name=table_name,
            table=table_name,
            key="Part ID",
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
    libraries.append(new_library)

kicad_dbl["libraries"] = libraries
kicad_dbl.save(KICAD_DBL_FILEPATH)