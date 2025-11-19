import csv

def write_metadata_csv(csv_path, records):
    """
    records = [
        {
            "record_id": int,
            "doc_no": int,
            "volume": int,
            "offset": int,
            "length": int,
            "img_count": int,
            "raw_hex": str
        },
        ...
    ]
    """

    columns = [
        "record_id",
        "doc_no",
        "volume",
        "offset",
        "length",
        "img_count",
        "raw_hex"
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()

        for r in records:
            writer.writerow(r)

    print(f"CSV exported → {csv_path}")