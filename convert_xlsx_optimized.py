import argparse
import json
import os

DICT_KEYS = ["quota", "institute", "course", "allottedCategory", "candidateCategory", "remarks"]
ROW_KEYS = ["sno", "rank", "quota", "institute", "course", "allottedCategory", "candidateCategory", "remarks"]


def load_rows(n):
    src = f"round-{n}/data.js"
    content = open(src, encoding="utf-8").read()
    rows = json.loads(content[content.index("=") + 1 :].strip().rstrip(";"))
    rows = [r for r in rows if not is_empty_row(r)]
    return rows


def is_empty_row(row):
    return all(not (row.get(k) or "").strip() for k in DICT_KEYS)


def build_indexes(rows):
    indexes = {}
    uniques = {}
    for key in DICT_KEYS:
        values = [row.get(key) or "" for row in rows]
        unique = sorted(set(values), key=lambda s: (s.casefold(), s))
        uniques[key] = unique
        indexes[key] = {v: i for i, v in enumerate(unique)}
    return indexes, uniques


def encode(rows, indexes):
    def idx(key, row):
        return indexes[key][row.get(key) or ""]

    return [
        [
            row.get("sno") or "",
            row.get("rank") or "",
            idx("quota", row),
            idx("institute", row),
            idx("course", row),
            idx("allottedCategory", row),
            idx("candidateCategory", row),
            idx("remarks", row),
        ]
        for row in rows
    ]


def decode(rows, uniques):
    q, i, c = uniques["quota"], uniques["institute"], uniques["course"]
    a, cc, r = uniques["allottedCategory"], uniques["candidateCategory"], uniques["remarks"]
    return [
        {
            "sno": row[0],
            "rank": row[1],
            "quota": q[row[2]],
            "institute": i[row[3]],
            "course": c[row[4]],
            "allottedCategory": a[row[5]],
            "candidateCategory": cc[row[6]],
            "remarks": r[row[7]],
        }
        for row in rows
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Dictionary-encode a round's data.js into data.compact.js"
    )
    parser.add_argument("--round", type=int, default=1, choices=[1, 2, 3])
    args = parser.parse_args()
    n = args.round
    out = f"round-{n}/data.compact.js"

    print(f"Reading round-{n}/data.js...")
    rows = load_rows(n)
    print(f"  {len(rows)} rows")

    print("Building dictionaries...")
    indexes, uniques = build_indexes(rows)
    for key in DICT_KEYS:
        print(f"  {key}: {len(uniques[key])} unique values")

    encoded = encode(rows, indexes)
    print(f"  encoded rows: {len(encoded)}")

    print("Verifying round-trip...")
    back = decode(encoded, uniques)
    assert len(back) == len(rows)
    for a, b in zip(back, rows):
        for key in ROW_KEYS:
            assert a[key] == b.get(key, ""), f"mismatch on {key}: {a[key]!r} != {b.get(key, '')!r}"
    print("  OK: decode(encode(data)) == data")

    print(f"Writing {out}...")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"const ROUND_{n}_DICT = ")
        json.dump(uniques, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
        f.write(f"const ROUND_{n}_DATA = ")
        json.dump(encoded, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")

    old = os.path.getsize(f"round-{n}/data.js")
    new = os.path.getsize(out)
    print(f"  {old/1e6:.2f} MB -> {new/1e6:.2f} MB ({new/old*100:.0f}% of original)")
    print("Done.")
