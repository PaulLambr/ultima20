import json
import pandas as pd
import gspread
from pathlib import Path
from google.oauth2.service_account import Credentials

# --- Setup credentials ---
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]
CREDS_FILE = "ledger-service-key.json"
SPREADSHEET_ID = "Monthly Ledger"
SHEET_NAME = "Summary"

# --- Authenticate ---
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
gc = gspread.authorize(creds)

# --- Load Sheet ---
sh = gc.open(SPREADSHEET_ID)  # Using title instead of ID
worksheet = sh.worksheet(SHEET_NAME)

# --- Extract DataFrame and filter ---
df = pd.DataFrame(worksheet.get_all_records())
df = df[["Date", "Net Total"]].dropna()

# --- Save to ~/Ledger_History/net_totals.json ---
output_path = Path.home() / "Ledger_History" / "net_totals.json"
with open(output_path, "w") as f:
    json.dump(df.to_dict(orient="records"), f, indent=2)

print(f"✅ Exported {len(df)} rows to {output_path}")
