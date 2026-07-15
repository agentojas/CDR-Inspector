# CDR-Inspector
Python Script for CDR analysis which Detects SIM replacement, Device changes, late-night calls, frequent contacts, long-duration calls, and other useful investigation patterns from CDR records.


# Features
- Detects SIM Replacement (IMSI change)
- Detects Device Change (IMEI change)
- Identifies Late Night Calls (11:00 PM – 6:00 AM)
- Reads the CDR Excel file from a user-provided path
- Generates a new Excel report with investigation results
- Prints a summary of detected events in the console

# Required Columns
- IMSI
- IMEI
- Call Start Time

# Output

The script creates a new Excel file containing:

- SIM Status
- Device Status
- Late Night Call
