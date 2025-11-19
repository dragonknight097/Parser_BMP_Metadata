import os
import parse_coi
import parse_fld
import parse_aud

#Path and output csv COI
path_coi = "Data Example/METADATA FILES/LEASING.COI"
output_csv_coi = "extractor/metadata_extractor/leasing_coi.csv"

path_fld = "Data Example/METADATA FILES/LEASING.FLD"
output_csv_fld = "extractor/metadata_extractor/leasing_fld.csv"

path_aud = "Data Example/METADATA FILES/LEASING.AUD"
output_csv_fld = "extractor/metadata_extractor/leasing_aud.csv"

def main():
    #Parse COI
    parse_coi.parse_coi(path_coi, output_csv_coi)

    #Parse FLD
    fields_fld = parse_fld.parse_fld(path_fld)
    parse_fld.export_csv_fld(fields_fld, output_csv_fld)

    #Parse AUD
    parse_aud.parse_aud(path_aud, path_fld, output_csv_fld)

if __name__ == "__main__":
    main()