import pandas as pd
from datetime import datetime
import os
import pandas as pd
from datetime import datetime

# ==============================
# Select Input File
# ==============================

input_file = input("Enter CDR Excel file path (.xlsx): ").strip().strip('"')

# Check file exists
if not os.path.exists(input_file):
    raise FileNotFoundError(f"File not found: {input_file}")

# Create output file in same folder
folder = os.path.dirname(input_file)
filename = os.path.splitext(os.path.basename(input_file))[0]

output_file = os.path.join(folder, filename + "_Analysis.xlsx")

print(f"\nInput File : {input_file}")
print(f"Output File: {output_file}\n")

# ==============================
# Read Excel
# ==============================
df = pd.read_excel(input_file)

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Check required columns
required_columns = ["IMSI", "IMEI", "Call Start Time"]

for col in required_columns:
    if col not in df.columns:
        raise Exception(f"Column '{col}' not found!")

# ====================================
# Reference IMSI & IMEI (First Row)
# ====================================
reference_imsi = str(df.loc[0, "IMSI"]).strip()
reference_imei = str(df.loc[0, "IMEI"]).strip()

# New Columns
df["SIM Status"] = ""
df["Device Status"] = ""
df["Late Night Call"] = ""

# ====================================
# Function to detect late-night calls
# ====================================
def is_late_night(value):

    if pd.isna(value):
        return False

    try:
        # Try parsing automatically
        t = pd.to_datetime(value).time()
    except:
        try:
            t = datetime.strptime(str(value), "%H:%M:%S").time()
        except:
            try:
                t = datetime.strptime(str(value), "%H:%M").time()
            except:
                return False

    # Between 23:00 and 06:00
    if t.hour >= 23 or t.hour < 6:
        return True

    return False


# ====================================
# Main Analysis
# ====================================
print("="*60)

for index, row in df.iterrows():

    current_imsi = str(row["IMSI"]).strip()
    current_imei = str(row["IMEI"]).strip()

    # --------------------------
    # SIM Replacement Detection
    # --------------------------
    if current_imsi != reference_imsi:
        df.at[index, "SIM Status"] = "SIM Replacement"

        print(f"[Row {index+2}] SIM Replacement")
        print(f"Previous IMSI : {reference_imsi}")
        print(f"Current  IMSI : {current_imsi}")
        print("-"*60)

    # --------------------------
    # Device Change Detection
    # --------------------------
    if current_imei != reference_imei:
        df.at[index, "Device Status"] = "Device Change"

        print(f"[Row {index+2}] Device Change")
        print(f"Previous IMEI : {reference_imei}")
        print(f"Current  IMEI : {current_imei}")
        print("-"*60)

    # --------------------------
    # Late Night Calls
    # --------------------------
    if is_late_night(row["Call Start Time"]):

        df.at[index, "Late Night Call"] = "YES"

        print(f"Late Night Call -> Row {index+2}")
        print(f"Time : {row['Call Start Time']}")
        print("-"*60)

# ====================================
# Summary
# ====================================
print("\nSUMMARY")
print("="*60)

print("SIM Replacements :", (df["SIM Status"] == "SIM Replacement").sum())
print("Device Changes   :", (df["Device Status"] == "Device Change").sum())
print("Late Night Calls :", (df["Late Night Call"] == "YES").sum())

# ====================================
# Save Result
# ====================================
df.to_excel(output_file, index=False)

print("\nSaved:", output_file)