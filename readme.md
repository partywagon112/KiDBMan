# KiCad Database Manager (KiDBMan)

An idea for a KiCad database editor to make it easier to manage the *.json file that describes the library.

Includes basic examples and pulls from the KiCad-libdb example database repository.

![Front Panel when starting with library](https://github.com/partywagon112/KiDBMan/blob/main/images/front_panel.png)

# What Works so Far
Can generate schememas and synchronise the database to the JSON, however want to add in a checkbox system to select what is visible, 
add/edit fields potentially?

# Future
Need a wizard to help construct database connection strings, as this is something that new users of the KiCad database library
will struggle with, and potentially an editor.

Would like to add in a library symbol adder, and potentially a method to synchronise the symbol and footprint libraries required for custom symbols/footprints.
The KiCad repositories have a method to track what is in a library, so it may be possible to perform santity checks that components referenced in the 
database exist, and can flag ones that do not.

Potentially would like to integrate in a default SQL Lite (Or other SQL version) to autogenerate the whole database, and create a rich editor,
but this is going to take a lot of time.
