# 📦 Packing List Generator

A desktop application that generates professional PDF packing lists from SAP Excel exports. Built with Python using Tkinter for the GUI, pandas for data processing, and fpdf2 for PDF generation.

## ✨ Features

- 📂 Browse and load SAP Excel export files (`.xlsx`)
- 🔍 Automatically validates, cleans, and groups data by package
- 📄 Generates a formatted A4 landscape PDF packing list with:
  - 🏢 Company header with logo
  - 🔢 Order and vendor information
  - 📊 Itemized table with weights and piece counts
  - ➕ Totals summary
  - 📑 Page numbers and company footer

## ⚙️ Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd packing_list_generator
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure the following asset folders exist in the project root:
   - `images/` — place your `logo.png` and `i.ico` here
   - `fonts/` — place `IBMPlexSans-Regular.ttf` and `IBMPlexSans-Bold.ttf` here

## 🖥️ Usage

Run the application with:

```bash
python main.py
```

Then:
1. Click **Browse** to select your SAP Excel export file
2. Enter the **Order** number and **Vendor** number
3. Pick a **Date** using the date picker
4. Click **Generate** to create the PDF 🎉

The output PDF will be saved in the project root directory, named `<Order>_<Date>.pdf`.

## 🗂️ Project Structure

```
packing_list_generator/
├── main.py             # Application entry point and main window
├── file_processor.py   # Excel loading, validation, and data processing
├── pdf_generator.py    # PDF layout and generation
├── widgets.py          # Custom Tkinter UI components
├── requirements.txt
├── images/
│   ├── logo.png
│   └── i.ico
└── fonts/
    ├── IBMPlexSans-Regular.ttf
    └── IBMPlexSans-Bold.ttf
```

## 🔧 Configuration

Company details (name, city, address) can be updated in the `settings_company` dictionary inside `file_processor.py`:

```python
settings_company = {
    'city': 'Your City',
    'company_name': 'Your Company Name',
    'address': 'Your Company Address'
}
```

Column mappings between the SAP export and the output PDF are configured in `settings_columns` in the same file.
