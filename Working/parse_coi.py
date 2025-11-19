import os
import csv
import struct

# ===== COI RECORD FORMAT =====
RECORD_SIZE = 128

def parse_coi(path, output_csv):

    filesize = os.path.getsize(path)

    if filesize % RECORD_SIZE != 0:
        print("WARNING: File size does not divide evenly by 128 bytes!")

    record_count = filesize // RECORD_SIZE

    print(f"Parsing COI: {path}")
    print(f"File size: {filesize:,} bytes")
    print(f"Total records: {record_count}\n")

    results = []

    with open(path, "rb") as f:
        for i in range(record_count):
            chunk = f.read(RECORD_SIZE)

            # ===== Decode fields (based on requirement spec) =====
            DOC_NO    = struct.unpack("<I",  chunk[0:4])[0]     # uint32
            VOLUME    = struct.unpack("<H",  chunk[4:6])[0]     # uint16
            OFFSET    = struct.unpack("<I",  chunk[6:10])[0]    # uint32
            LENGTH    = struct.unpack("<I",  chunk[10:14])[0]   # uint32
            IMG_COUNT = struct.unpack("<H",  chunk[14:16])[0]   # uint16
            IMG_TYPE  = chunk[16]                               # 1 byte
            FLAGS     = chunk[17]                               # 1 byte

            # Remaining bytes (for debug)
            RESERVED  = chunk[18:].hex().upper()

            # Make row
            results.append({
                "Record#": i,
                "DOC_NO": DOC_NO,
                "VOLUME": VOLUME,
                "OFFSET": OFFSET,
                "LENGTH": LENGTH,
                "IMG_COUNT": IMG_COUNT,
                "IMG_TYPE": IMG_TYPE,
                "FLAGS": FLAGS,
                "RESERVED_HEX": RESERVED
            })

    # ===== Write CSV =====
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    print(f"COI parsed successfully.")
    print(f"CSV saved at: {output_csv}")