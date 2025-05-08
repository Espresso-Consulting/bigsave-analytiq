import pandas as pd

EXCEL_FILE = "Espresso Test Data.xlsx"

# Load the Excel file
xls = pd.ExcelFile(EXCEL_FILE)

# Print sheet names and count
print("Sheet names:", xls.sheet_names)
print("Number of sheets:", len(xls.sheet_names))

# Print columns for each sheet
for sheet in xls.sheet_names:
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet, nrows=0)
    print(f"\nSheet: {sheet}")
    print(f"Columns: {list(df.columns)}")
