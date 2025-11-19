import struct
import csv
import re
from pathlib import Path
import sys
import parse_fld

def read_aud_header(aud_bytes):
        # AUD header structure (first 8 bytes):
    #   offset 0–3 : uint32 LE → total file size
    #   offset 4–7 : uint32 LE → header length
    #
    # Both fields are stored in little-endian format.
    # file_size  = entire AUD file size as stored by the system
    # header_len = length of the fixed header before variable descriptors begin
    file_size = struct.unpack_from("<I", aud_bytes, 0)[0]   #little-endian
    header_len = struct.unpack_from("<I", aud_bytes, 4)[0]

    return file_size, header_len

def find_descriptor_start(aud_bytes, header_len):
    # Scan forward after the fixed header region (0 → header_len-1)
    # AUD files often store a padding area of zero bytes before
    # the actual descriptor block begins.
    #
    # This function finds the first NON-zero byte after header_len,
    # which indicates the real start of the descriptor section.
    for i in range(header_len, len(aud_bytes)):
        if aud_bytes[i] != 0:
            return i
        
def parse_descriptor_uint16(aud_bytes, start_offset, count):
    # Read "count" uint16 values (2 bytes each) starting at start_offset.
    # Each value = unsigned short, little-endian.
    # Step = +2 bytes per entry.
    lengths = []
    for i in range(count):
        val = struct.unpack_from("<H", aud_bytes, start_offset + i * 2)[0]
        lengths.append(val)
    return lengths

def build_schema(names, lengths):
    # Build schema entries:
    # n = field name
    # l = field length (bytes)
    # off = current byte offset for this field
    schema = []
    off = 0
    for n, l in zip(names, lengths):
        schema.append((n, l, off))
        off += l
    return schema

def save_schema_csv(schema, outpath):
    # Save schema list into CSV.
    # schema = list of (field_name, field_length, field_offset)
    # CSV columns: field_name, length, offset
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["field_name", "length", "offset"])
        for name, length, offset in schema:
            w.writerow([name, length, offset])
    print(f"AUD parsed successfully.")

def parse_aud(aud_path, fld_path, out_csv):
    aud_bytes = Path(aud_path).read_bytes()

    names = parse_fld.parse_fld(fld_path)

    file_size, header_len = read_aud_header(aud_bytes)

    desc_start = find_descriptor_start(aud_bytes, header_len)

    lengths = parse_descriptor_uint16(aud_bytes, desc_start, len(names))

    schema = build_schema(names, lengths)

    save_schema_csv(schema, out_csv)

    return schema


