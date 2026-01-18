import tkinter as tk
from tkinter import ttk 
from tkinter.filedialog import askopenfilename
from tkcalendar import Calendar, DateEntry
import datetime



class FileBrowser(tk.Frame):
    FILE_TYPES = [('Excel Files', '*.xlsx')]
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # widgets
        self.browse_button = ttk.Button(self, text='Browse', command=self.open_file)
        self.browse_button.grid(row=0, column=1)

        self.file_entry = ttk.Entry(self, width=40, validate='key', textvariable=self.master.file_path)
        self.file_entry.grid(row=0, column=0)


    def open_file(self):
        filename = askopenfilename(filetypes=self.FILE_TYPES)
        if filename:
            return self.master.file_path.set(filename)



class InputEntry(tk.Frame):
    def __init__(self, master, name, var):
        super().__init__(master)
        self.master = master
        self.name = name
        self.var = var
        
        # config 
        self.columnconfigure(0, weight=1, uniform='B')
        self.columnconfigure(1, weight=3, uniform='B')

        # widgets
        self.label = tk.Label(self, text=self.name)
        self.label.grid(row=1, column=0, sticky='w')

        self.entry = ttk.Entry(self, textvariable=self.var, width=15)
        self.entry.grid(row=1, column=1, sticky='we')



class DatePicker(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # config
        self.columnconfigure(0, weight=1, uniform='B')
        self.columnconfigure(1, weight=2, uniform='B') 

        # widgets
        self.label = tk.Label(self, text='Date')
        self.label.grid(row=0, column=0, sticky='w')

        self.calendar = DateEntry(self, width=12)
        self.calendar.grid(row=0, column=1, sticky='we')

        self.master.date.set(self.calendar.get_date())
        self.calendar.bind('<<DateEntrySelected>>',self.my_upd)


    def my_upd(self, *args):
        self.date = self.calendar.get_date()
        self.master.date.set(self.date.strftime('%d.%m.%Y'))