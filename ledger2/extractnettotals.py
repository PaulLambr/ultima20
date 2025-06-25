import json
from pathlib import Path
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# === CONFIGURATION ===
OUTPUT_PATH = Path.home() / "Ledger_History" / "net_totals.json"
CREDS_FILE = "ledger-service-key.json"
SPREADSHEET_TITLE = "Monthly Ledger"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

sh = client.open(SPREADSHEET_TITLE)

# === Summary chart data ===
summary_df = pd.DataFrame(sh.worksheet("Summary").get_all_records())
chart_data = summary_df[["Date", "Net Total"]].dropna().to_dict(orient="records")

# === Init snapshot object ===
latest_snapshot = {
    "timestamp": None,
    "netTotal": None,
    "assetTotal": None,
    "billTotal": None,
    "assets": [],
    "ledger": [],
    "error": None
}

# === Get latest snapshot filename ===
filenames = sh.worksheet("IngestedFiles").col_values(1)
latest_file = filenames[-1] if filenames else None

def get_column(df, name):
    for col in df.columns:
        if col.strip().lower() == name:
            return col
    return None

if latest_file:
    try:
        matching_tab = latest_file.replace(".json", "")
        all_titles = [ws.title for ws in sh.worksheets()]
        if matching_tab not in all_titles:
            raise Exception(f"❌ Tab '{matching_tab}' not found.")

        snap_df = pd.DataFrame(sh.worksheet(matching_tab).get_all_records())
        split_index = snap_df[snap_df.isnull().all(axis=1)].index

        if not split_index.empty:
            asset_df = snap_df.iloc[:split_index[0]].reset_index(drop=True)
            ledger_df = snap_df.iloc[split_index[0]+1:].reset_index(drop=True)
        else:
            asset_df = snap_df
            ledger_df = pd.DataFrame()

        asset_amt_col = get_column(asset_df, "amount")
        ledger_amt_col = get_column(ledger_df, "amount") if not ledger_df.empty else None

        asset_df[asset_amt_col] = pd.to_numeric(asset_df[asset_amt_col], errors="coerce").fillna(0).astype(int)
        if not ledger_df.empty:
            ledger_df[ledger_amt_col] = pd.to_numeric(ledger_df[ledger_amt_col], errors="coerce").fillna(0).astype(int)

        # === CLEAN ===
        asset_df = asset_df[
            (asset_df.get("name", "").astype(str).str.strip().str.lower() != "name") &
            (asset_df.get("name", "").astype(str).str.strip() != "") &
            (asset_df[asset_amt_col] > 0)
        ].reset_index(drop=True)

        if not ledger_df.empty:
            ledger_df = ledger_df[
                (ledger_df.get("name", "").astype(str).str.strip().str.lower() != "name") &
                (ledger_df.get("name", "").astype(str).str.strip() != "") &
                (ledger_df[ledger_amt_col] > 0)
            ].reset_index(drop=True)

        latest_snapshot.update({
            "timestamp": matching_tab,
            "assets": asset_df.to_dict(orient="records"),
            "ledger": ledger_df.to_dict(orient="records"),
            "assetTotal": int(asset_df[asset_amt_col].sum()),
            "billTotal": int(ledger_df[ledger_amt_col].sum()) if not ledger_df.empty else 0
        })
        latest_snapshot["netTotal"] = latest_snapshot["assetTotal"] - latest_snapshot["billTotal"]

    except Exception as e:
        latest_snapshot["error"] = str(e)

# === Save result ===
with open(OUTPUT_PATH, "w") as f:
    json.dump({
        "chartData": chart_data,
        "latestSnapshot": latest_snapshot
    }, f, indent=2)

print(f"✅ Exported full data to {OUTPUT_PATH}")
