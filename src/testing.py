import kidbman
from kidbman.libdb_reader import DatabaseDescription
from kidbman.database_reader import LibraryDatabase


# print(pyodbc.drivers())


# DatabaseDescription

# print(database.tables)

kicad_dbl = DatabaseDescription("configuration.kicad_dbl")

resistor_library = kicad_dbl.get_library("Resistors")
resistor_library["key"] = "Cheese"
kicad_dbl.set_library(resistor_library)
kicad_dbl.save("configuration2.kicad_dbl")

# database = LibraryDatabase.from_source(kicad_dbl['source'])

# print(database.get_table_names())
# print(database.get_table_fields('TestTable'))