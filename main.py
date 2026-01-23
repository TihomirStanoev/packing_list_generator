import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
import re
from pathlib import Path
from widgets import FileBrowser, InputEntry, DatePicker
from file_processor import FileProccessor
from os import path
from pdf_generator import PdfGenerator



class App(tk.Tk):
    def __init__(self):
        # setup
        super().__init__()
        self.geometry('390x110')
        self.title('Packing List Generator')
        self.resizable(False, False)
        self.rowconfigure((0,1,2), weight=1, uniform=1)
        self.columnconfigure(list(range(4)), weight=1, uniform='A')
        self.iconbitmap(resource_path(path.join('images', 'i.ico')))
        self.file_proccessor = FileProccessor()

        # vars 
        self.file_path = tk.StringVar()
        self.order = tk.StringVar(value='')
        self.vendor = tk.StringVar(value='')
        self.date = tk.StringVar()


        self.table = None

        self.frame_data = {
            'Order': {'variable': self.order, 'rex': r''},
            'Vendor': {'variable': self.vendor, 'rex': r''}
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
        date = self.date.get()
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
        
        return self.create_pdf(order, vendor, date, self.file_proccessor.totals)



    def create_pdf(self, order, vendor, date, totals):
        pdf_generator = PdfGenerator(order, vendor, date, totals)
        pdf_generator.totals = self.file_proccessor.totals


        try:
            pdf_generator.generate_from_df(self.file_proccessor.df)
        except Exception as e:
            return messagebox.showerror('Грешка при генериране', str(e))
        
        return messagebox.showinfo('Успешно генериране!', 'Пакинг листа е генериран успешно!')


        




if __name__ == "__main__":
    app = App()
    app.mainloop()
