import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *

app = ttk.Window(themename="superhero")

columns = [
    {"text": "LicenseNumber", "stretch": False},
    {"text": "Company Name", "stretch": False},
    {"text": "User Count", "stretch": False}
]

row_data = [
    ("A123", "izzyco", 123),
    ("A456", "asdf", 129),
    ("A789", "what", 128)
]

table = Tableview(
    master=app,
    coldata=columns,
    rowdata=row_data,
    paginated=True,
    autofit=True,
    searchable=True,
    bootstyle=PRIMARY,
    stripecolor=(app.style.colors.light, 'green')
)

table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
table.insert_row('end', ['Marzale LLC, 26'])
table.load_table_data()

# b1 = ttk.Button(app, text="Button 1", bootstyle=SUCCESS)
# b1.pack(side=LEFT, padx=5, pady=10)

# b2 = ttk.Button(app, text="Button 2", bootstyle=(INFO, OUTLINE))
# b2.pack(side=LEFT, padx=5, pady=10)

app.mainloop()