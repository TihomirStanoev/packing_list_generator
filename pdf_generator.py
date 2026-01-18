from fpdf import FPDF
import pandas as pd





def pdf_generator(df):
    
    pdf = FPDF(orientation="landscape", format="A4")
    pdf.add_page()
    column_widths = (12, 12, 6, 12, 35, 8, 12, 13) 

    pdf.set_font("Times", size=10)
    with pdf.table(
        col_widths=column_widths,
        borders_layout="HORIZONTAL_LINES",
        cell_fill_color=(240, 240, 240), 
        cell_fill_mode="ROWS",
        line_height=8,
        text_align=("CENTER", "CENTER", "CENTER", "CENTER", "LEFT", "CENTER", "RIGHT", "RIGHT"), 
    ) as table:
        
        pdf.set_font("Times", style="B", size=11)
        header_row = table.row()
        for col in df.columns:
            header_row.cell(col)
        
        pdf.set_font("Times", style="", size=10)
        for _, data_row in df.iterrows():
            row = table.row()
            for i, datum in enumerate(data_row):
                val = str(datum)
                if isinstance(datum, (float, int)) and i > 3:
                    val = f"{datum:.3f}" if isinstance(datum, float) else str(datum)
                
                row.cell(val)

    pdf.output("table.pdf")


