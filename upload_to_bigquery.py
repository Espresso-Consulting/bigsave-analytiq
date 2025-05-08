import os
import pandas as pd
from google.cloud import bigquery

# === CONFIGURATION ===
EXCEL_FILE = "Espresso Test Data.xlsx"
SERVICE_ACCOUNT_FILE = "bigsave-6767d8651634.json"
PROJECT_ID = "bigsave"
DATASET_ID = "demo"

# === AUTHENTICATION ===
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_FILE
client = bigquery.Client(project=PROJECT_ID)

print(f"Loading {EXCEL_FILE}...")
xls = pd.ExcelFile(EXCEL_FILE)
sheet_names = xls.sheet_names
print(f"Found {len(sheet_names)} sheets: {sheet_names}")

for sheet in sheet_names:
    print(f"Processing sheet: {sheet}")
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)

    # Convert all columns to string to avoid type inference issues
    for col in df.columns:
        df[col] = df[col].astype(str)

    print(f"Read {len(df)} rows and {len(df.columns)} columns.")

    # Sanitize table name: remove spaces and lowercase
    table_name = sheet.strip().replace(' ', '_').lower()
    full_table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    # === CONFIGURE LOAD JOB ===
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # Overwrites table
        autodetect=True,                     # Infers schema
    )

    # === UPLOAD ===
    print(f"Uploading to BigQuery table: {full_table_id}...")
    load_job = client.load_table_from_dataframe(df, full_table_id, job_config=job_config)
    load_job.result()

    print(f"✅ Upload complete for {full_table_id}.")
