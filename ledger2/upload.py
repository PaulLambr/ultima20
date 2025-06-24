import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

# === CONFIG ===
EXCEL_PATH = Path.home() / "Ledger_History" / "monthly_ledger.xlsx"
SHEET_TITLE = "Monthly Ledger"
SERVICE_KEY_PATH = "ledger-service-key.json"

# === SETUP GOOGLE CLIENT ===
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file(SERVICE_KEY_PATH, scopes=scopes)
client = gspread.authorize(creds)

# === LOAD OR CREATE GOOGLE SHEET ===
try:
    sh = client.open(SHEET_TITLE)
except gspread.SpreadsheetNotFound:
    sh = client.create(SHEET_TITLE)
    sh.share("your.email@gmail.com", perm_type="user", role="writer")  # Optional

# === LOAD EXCEL FILE ===
xls = pd.ExcelFile(EXCEL_PATH)

# === SYNC EACH TAB TO GOOGLE SHEETS ===
for sheet_name in xls.sheet_names:
    df = xls.parse(sheet_name)

    # Delete sheet if exists
    try:
        existing = sh.worksheet(sheet_name)
        sh.del_worksheet(existing)
    except gspread.exceptions.WorksheetNotFound:
        pass

    # Create new sheet & update content
    worksheet = sh.add_worksheet(title=sheet_name, rows=str(len(df)+10), cols=str(len(df.columns)+5))
    # Clean any NaNs before pushing to Sheets
    clean_df = df.fillna("")  # or .fillna(0) if numeric zero makes more sense

    # Push to sheet
    worksheet.update([clean_df.columns.tolist()] + clean_df.values.tolist())


print(f"✅ Synced {len(xls.sheet_names)} tab(s) to Google Sheet: {SHEET_TITLE}")
