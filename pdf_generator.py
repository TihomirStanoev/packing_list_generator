from fpdf import FPDF
import pandas as pd
from file_processor import DfConfigMixin
import os



class PdfGenerator(FPDF, DfConfigMixin):
    def __init__(self, 
                 order: str = '', 
                 vendor: str = '', 
                 date: str = '', 
                 totals=None, 
                 city: str = 'CITY',
                 company_name: str = 'STREET',
                 address: str = 'ADDRESS'):
        
        super().__init__(orientation="L", unit="mm", format="A4")
        self.order = order
        self.vendor = vendor
        self.date = date
        self.totals = totals if totals else {}
        self.city = city
        self.company_name = company_name
        self.address = address
        self.logo_path = os.path.join('images', 'logo.png')

        try:
            r_font_path = os.path.join('fonts', 'IBMPlexSans-Regular.ttf')
            b_font_path = os.path.join('fonts', 'IBMPlexSans-Bold.ttf')
            
            self.add_font("Roboto", style="", fname=r_font_path)
            self.add_font("Roboto", style="B", fname=b_font_path)
        except Exception as e:
            print(e)

    def header(self):
        self.image(self.logo_path, 10, 5, 45, keep_aspect_ratio=True)
        
        self.set_font("Roboto", style="B", size=14)
        self.set_xy(0, 10)
        self.cell(0, 10, f"{self.city}, {self.date}", align='C')
        
        self.set_font("Roboto",  size=9)
        self.set_xy(-40, 10)
        self.cell(30, 10, f"Page {self.page_no()} of {{nb}}", align='R')

        right_block_x = self.w - 120
        self.set_xy(right_block_x, 30)
        
        self.set_font("Roboto", style="B", size=10)
        self.cell(30, 5, "SHIP-TO-PARTY:")
        self.set_font("Roboto", style="", size=10)
        self.cell(0, 5, f" {self.vendor}", ln=1)
        
        self.set_x(right_block_x)
        self.set_font("Roboto", style="B", size=10)
        self.cell(30, 5, "ORDER:")
        self.set_font("Roboto", size=10)
        self.cell(30, 5, f"{self.order}", ln=1)

        self.ln(5)
        self.set_font("Roboto", style="B", size=14)
        self.cell(0, 10, "WEIGHT NOTE PACKING LIST", align='C', ln=1)
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_x(10)
        self.set_font("Roboto", style="B", size=9)
        self.cell(0, 5, self.company_name, ln=1)
        self.set_font("Roboto", style="", size=8)
        self.cell(0, 5, self.address)

    def generate_from_df(self, df):
        self.alias_nb_pages() 
        self.add_page()


        column_widths = self._column_widths 
        
        self.set_font("Roboto", style="B", size=9)
        with self.table(
            col_widths=column_widths,
            borders_layout="HORIZONTAL_LINES",
            cell_fill_color=(255, 255, 255),
            line_height=7,
        ) as table:
            header_row = table.row()
            for col in df.columns:
                header_row.cell(col)

            self.set_font("Roboto", size=8)
            for _, data_row in df.iterrows():
                row = table.row()
                num_cols = len(data_row)
                for i, datum in enumerate(data_row):
                    val = str(datum)
                    if isinstance(datum, (float, int)) and i >= (num_cols - 3):
                        val = f"{datum:,.3f}" if isinstance(datum, float) else f"{datum:,}"

                    row.cell(val)

        self.ln(10)
        right_align_x = self.w - self.l_margin - 70 
        
        for key, value in self.totals.items():
            self.set_x(right_align_x)
            self.set_font("Roboto", style="", size=9)
            self.cell(40, 8, f"{key.upper()}:", align='L')
            
            self.set_font("Roboto", style="B", size=9)
            val_text = f"{value:,.3f}" if isinstance(value, (float, int)) else str(value)
            self.cell(30, 8, val_text, align='R', ln=1)

        file_name = f"{self.order}_{self.date.replace('.', '-')}.pdf"
        self.output(file_name)

