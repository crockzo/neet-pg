import time
from pathlib import Path

import pandas as pd
from openpyxl import Workbook

# ===========================================
# Configuration
# ===========================================

INPUT_FOLDER = str(input("Enter folder name which contains the excel files, eg : all-excel"))
OUTPUT_FILE = "merged.xlsx"

# ===========================================


def main():

    start = time.time()

    print("=" * 60)
    print("EXCEL MERGER")
    print("=" * 60)

    input_dir = Path(INPUT_FOLDER)

    if not input_dir.exists():
        print(f"❌ Folder not found: {INPUT_FOLDER}")
        return

    excel_files = sorted(input_dir.glob("*.xlsx"))

    if len(excel_files) == 0:
        print("❌ No Excel files found.")
        return

    print(f"📂 Found {len(excel_files)} Excel files.\n")

    wb = Workbook()
    ws = wb.active
    ws.title = "Merged"

    current_row = 1

    for index, excel_file in enumerate(excel_files, start=1):

        print(f"[{index}/{len(excel_files)}] Reading {excel_file.name}")

        try:

            df = pd.read_excel(
                excel_file,
                sheet_name=0,
                header=None
            )

            print(f"    Rows: {len(df)}")

            # Write filename as separator
            ws.cell(row=current_row, column=1).value = f"===== {excel_file.stem} ====="
            current_row += 1

            # Write data
            for row in df.itertuples(index=False):
                for col, value in enumerate(row, start=1):
                    ws.cell(row=current_row, column=col).value = value
                current_row += 1

            # Blank row between files
            current_row += 2

            print("    ✅ Done")

        except Exception as e:
            print(f"    ❌ Failed: {e}")

    print("\nSaving merged workbook...")

    wb.save(OUTPUT_FILE)

    elapsed = time.time() - start

    print(f"✅ Saved: {OUTPUT_FILE}")
    print(f"⏱ Total Time: {elapsed:.2f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()
