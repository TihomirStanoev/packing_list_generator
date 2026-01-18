import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
import re
from pathlib import Path
from widgets import FileBrowser, InputEntry, DatePicker
from file_processor import FileProccessor
from os import path
from pdf_generator import pdf_generator



class App(tk.Tk):
    def __init__(self):
        # setup
        super().__init__()
        self.geometry('390x110')
        self.title('Packing List Generator')
        self.resizable(False, False)
        self.rowconfigure((0,1,2), weight=1, uniform=1)
        self.columnconfigure(list(range(4)), weight=1, uniform='A')
        self.iconbitmap(path.join('images','i.ico'))
        
        # vars 
        self.file_path = tk.StringVar()
        self.order = tk.StringVar(value='')
        self.vendor = tk.StringVar(value='')
        self.date = tk.StringVar()

        self.file_proccessor = FileProccessor()
        self.table = None

        self.frame_data = {
            'Order': {'variable': self.order, 'rex': r'^82\d{8}$'},
            'Vendor': {'variable': self.vendor, 'rex': r'^\d{9}[А-зA-z0-9 ]+$'}
        }

        # widgets
        self.entry_frame = []

        self.file_browser = FileBrowser(self)
        self.file_browser.grid(row=0, column=0, columnspan=4)

        self.date_picker = DatePicker(self)
        self.date_picker.grid(row=2, column=0, columnspan=2, sticky='w')

        self.generate = ttk.Button(self, text='Generate', command=self.generate)
        self.generate.grid(row=2, column=3, sticky='n')

        for i, (name, configs) in enumerate(self.frame_data.items()):
            entry = InputEntry(self, name, configs['variable'])
            entry.grid(row=1, column=i * 2, columnspan=2)
            self.entry_frame.append(entry)
      


    def generate(self):
        order = self.order.get()
        vendor = self.vendor.get()
        filepath = Path(self.file_path.get())

        if not filepath.is_file():
            return messagebox.showerror('Error', 'Невалиден файл!')
        if not re.match(self.frame_data['Order']['rex'], order):
            return messagebox.showerror('Error', 'Невалидна поръчка!')
        if not re.match(self.frame_data['Vendor']['rex'], vendor):
            return messagebox.showerror('Error', 'Невалиден вендорен номер!')

        try:
            self.file_proccessor.load_file(filepath)
            self.file_proccessor.process_file()
        except Exception as e:
            return messagebox.showerror('Грешка при обработка', str(e))

        print(self.file_proccessor.df)
        print(self.file_proccessor.totals)
        print('----')
        print(f'File: {self.file_path.get()}, Vendor: {self.vendor.get()}, Order: {self.order.get()}, Date: {self.date.get()}')
        pdf_generator(self.file_proccessor.df)


        




if __name__ == "__main__":
    app = App()
    app.mainloop()