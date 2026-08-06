import argparse
import json
import re
import xml.etree.ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
XLSX = "neet-pg-document.xlsx"
OUT = "data.js"

KEY_BY_COL = {
    "A": "sno",
    "B": "rank",
    "C": "quota",
    "D": "institute",
    "E": "course",
    "F": "allottedCategory",
    "G": "candidateCategory",
    "H": "remarks",
}

ROUND = 3
XLSX = "neet-pg-document.xlsx"
OUT = "data.js"
VAR = "ALLOTMENT_DATA"


def load_shared_strings():
    strings = []
    import zipfile
    with zipfile.ZipFile(XLSX) as z:
        with z.open("xl/sharedStrings.xml") as f:
            for _, elem in ET.iterparse(f, events=("end",)):
                if elem.tag == NS + "si":
                    text = "".join(
                        t.text or "" for t in elem.iter(NS + "t")
                    )
                    strings.append(text)
                    elem.clear()
    return strings


def load_rows():
    import zipfile
    rows = []
    with zipfile.ZipFile(XLSX) as z:
        with z.open("xl/worksheets/sheet1.xml") as f:
            for _, elem in ET.iterparse(f, events=("end",)):
                if elem.tag == NS + "row":
                    row = {}
                    for c in elem.iter(NS + "c"):
                        col = c.get("r")[0]
                        key = KEY_BY_COL.get(col)
                        if key is None:
                            continue
                        v = c.find(NS + "v")
                        if v is None or v.text is None:
                            row[key] = ""
                            continue
                        if c.get("t") == "s":
                            row[key] = re.sub(r"\s+", " ", shared_strings[int(v.text)]).strip()
                        else:
                            val = v.text
                            if re.fullmatch(r"-?\d+\.0", val):
                                val = val[:-2]
                            row[key] = val
                    rows.append(row)
                    elem.clear()
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rebuild a round's data.js from its neet-pg-document.xlsx"
    )
    parser.add_argument(
        "--round", type=int, default=2, choices=[1, 2],
        help="Counseling round number (writes round-N/data.js with ROUND_N_DATA)",
    )
    args = parser.parse_args()
    ROUND = args.round
    XLSX = f"round-{ROUND}/neet-pg-document.xlsx"
    OUT = f"round-{ROUND}/data.js"
    VAR = f"ROUND_{ROUND}_DATA"

    print("Reading shared strings...")
    shared_strings = load_shared_strings()
    print(f"  {len(shared_strings)} strings loaded")

    print("Parsing sheet rows...")
    rows = load_rows()
    print(f"  {len(rows)} rows parsed (incl. header)")

    header = rows[0]
    assert header["sno"] == "SNo", "Unexpected first row, header handling wrong"
    rows = rows[1:]
    print(f"  {len(rows)} data rows (header excluded)")

    print(f"Writing {OUT}...")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(f"const {VAR} = ")
        json.dump(rows, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")

    print("Done.")
    for r in rows[:3]:
        print("  sample:", r)
    if rows:
        print("  last row:", rows[-1])
