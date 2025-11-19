import re
import csv
from pathlib import Path

def parse_fld(path):
    data = Path(path).read_bytes() #open the files with binary

    fields = [
        m.group(0).decode("latin1") #convert byte to string
        for m in re.finditer(rb"[ -~]{4,}", data) #find string ASCII
    ]

    return fields

def export_csv_fld(fields, output_csv):
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["field_name"])
        for name in fields:
            w.writerow([name])
    print(f"FLD parsed successfully.")
    print(f"CSV saved at: {output_csv}")
