import os
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

import camelot
import pandas as pd
from pypdf import PdfReader


# ===================================================
# Configuration
# ===================================================

INPUT_FOLDER = "split_parts" #str(input("Enter folder name which contains pdf file's. eg : pdfs"))
OUTPUT_FOLDER = "output"

TABLE_FLAVOR = "lattice"

# None = automatically use number of CPU cores
MAX_WORKERS = 4

# ===================================================


def process_pdf(pdf_path: Path):

    pdf_name = pdf_path.stem
    output_excel = Path(OUTPUT_FOLDER) / f"{pdf_name}.xlsx"

    start = time.time()

    print(f"\n[{pdf_name}] Started")

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)

    print(f"[{pdf_name}] Pages : {total_pages}")

    all_tables = []
    total_tables = 0

    for page in range(1, total_pages + 1):

        print(
            f"[{pdf_name}] Page {page}/{total_pages}",
            flush=True
        )

        try:

            tables = camelot.read_pdf(
                str(pdf_path),
                pages=str(page),
                flavor=TABLE_FLAVOR,
            )

            print(
                f"[{pdf_name}] Found {len(tables)} tables",
                flush=True
            )

            for table in tables:

                all_tables.append(table.df)
                all_tables.append(pd.DataFrame())

                total_tables += 1

        except Exception as e:

            print(
                f"[{pdf_name}] ERROR Page {page}: {e}",
                flush=True
            )

    if len(all_tables) == 0:

        print(f"[{pdf_name}] No tables detected")

        return pdf_name, 0, total_pages

    current_row = 0

    with pd.ExcelWriter(
        output_excel,
        engine="openpyxl"
    ) as writer:

        for df in all_tables:

            if df.empty:
                current_row += 1
                continue

            df.to_excel(
                writer,
                sheet_name="Tables",
                startrow=current_row,
                index=False,
                header=False
            )

            current_row += len(df) + 1

    elapsed = time.time() - start

    print(
        f"[{pdf_name}] Finished "
        f"({total_tables} tables, {elapsed:.1f}s)"
    )

    return pdf_name, total_tables, total_pages


def main():

    Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

    pdf_files = sorted(Path(INPUT_FOLDER).glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    print("=" * 60)
    print("Camelot Parallel Extractor")
    print("=" * 60)

    print(f"Found {len(pdf_files)} PDFs\n")

    overall_start = time.time()

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = {
            executor.submit(process_pdf, pdf): pdf
            for pdf in pdf_files
        }

        completed = 0

        for future in as_completed(futures):

            completed += 1

            try:

                pdf_name, tables, pages = future.result()

                print(
                    "\n"
                    + "=" * 60
                )

                print(
                    f"Completed {completed}/{len(pdf_files)}"
                )

                print(f"PDF     : {pdf_name}")

                print(f"Pages   : {pages}")

                print(f"Tables  : {tables}")

                print("=" * 60)

            except Exception as e:

                print(f"FAILED : {e}")

    total_time = time.time() - overall_start

    print("\n")
    print("=" * 60)
    print("ALL PDFs FINISHED")
    print(f"Total Time : {total_time:.2f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()
