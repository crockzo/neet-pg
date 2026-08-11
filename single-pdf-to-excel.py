import os
import time

import camelot
import pandas as pd
from pypdf import PdfReader


# ==========================
# Configuration
# ==========================

PDF_FILE = str(input("Enter pdf file name with .pdf at the end. eg : document.pdf"))
OUTPUT_EXCEL = "output.xlsx"

# flavor = "lattice"  -> bordered tables
# flavor = "stream"   -> borderless tables
TABLE_FLAVOR = "lattice"


# ==========================
# Main
# ==========================

def main():
    start = time.time()

    print("=" * 60)
    print(" PDF TO EXCEL TABLE EXTRACTOR ")
    print("=" * 60)

    if not os.path.exists(PDF_FILE):
        print(f"\n❌ PDF not found: {PDF_FILE}")
        return

    print(f"\n📄 Opening PDF: {PDF_FILE}")

    reader = PdfReader(PDF_FILE)
    total_pages = len(reader.pages)

    print(f"✅ Total Pages: {total_pages}")
    print()

    all_tables = []

    total_table_count = 0

    for page in range(1, total_pages + 1):

        print("-" * 60)
        print(f"📖 Processing Page {page}/{total_pages}")

        page_start = time.time()

        try:
            tables = camelot.read_pdf(
                PDF_FILE,
                pages=str(page),
                flavor=TABLE_FLAVOR
            )

            print(f"   Tables detected: {len(tables)}")

            if len(tables) == 0:
                print("   No tables found.")
                continue

            for index, table in enumerate(tables, start=1):

                df = table.df

                print(
                    f"      Table {index}: "
                    f"{df.shape[0]} rows × {df.shape[1]} columns"
                )

                all_tables.append(df)

                # blank row between tables
                all_tables.append(pd.DataFrame())

                total_table_count += 1

        except Exception as e:
            print(f"   ❌ Error on page {page}")
            print(e)

        elapsed = time.time() - page_start
        print(f"   Finished page in {elapsed:.2f} sec")

    print("\n" + "=" * 60)
    print("Writing Excel...")

    if len(all_tables) == 0:
        print("❌ No tables found in the PDF.")
        return

    current_row = 0

    with pd.ExcelWriter(
        OUTPUT_EXCEL,
        engine="openpyxl"
    ) as writer:

        sheet_name = "Tables"

        for df in all_tables:

            if df.empty:
                current_row += 1
                continue

            df.to_excel(
                writer,
                sheet_name=sheet_name,
                startrow=current_row,
                index=False,
                header=False
            )

            current_row += len(df) + 1

    print(f"✅ Excel saved as: {OUTPUT_EXCEL}")
    print(f"✅ Total tables extracted: {total_table_count}")

    total_time = time.time() - start
    print(f"⏱ Total time: {total_time:.2f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()
