import time
from pathlib import Path
from pypdf import PdfReader, PdfWriter

# ==================================================
# Configuration
# ==================================================

INPUT_PDF = str(input("Enter pdf file name with .pdf : "))
OUTPUT_PDF = "extracted_pages.pdf"

# Enter the exact page numbers you want (1-based indexing)
PAGES_TO_EXTRACT = [4]

# ==================================================


def main():

    start = time.time()

    print("=" * 60)
    print("PDF PAGE EXTRACTOR")
    print("=" * 60)

    input_path = Path(INPUT_PDF)

    if not input_path.exists():
        print(f"❌ File not found: {INPUT_PDF}")
        return

    print(f"📄 Reading: {INPUT_PDF}")

    reader = PdfReader(INPUT_PDF)
    total_pages = len(reader.pages)

    print(f"✅ Total Pages: {total_pages}")
    print(f"📑 Requested Pages: {PAGES_TO_EXTRACT}")
    print()

    writer = PdfWriter()

    extracted = 0

    for page in PAGES_TO_EXTRACT:

        if page < 1 or page > total_pages:
            print(f"⚠ Skipping invalid page: {page}")
            continue

        print(f"✅ Extracting page {page}")

        writer.add_page(reader.pages[page - 1])
        extracted += 1

    if extracted == 0:
        print("\n❌ No valid pages selected.")
        return

    print("\n💾 Saving output PDF...")

    with open(OUTPUT_PDF, "wb") as f:
        writer.write(f)

    elapsed = time.time() - start

    print(f"✅ Saved: {OUTPUT_PDF}")
    print(f"📄 Pages Extracted: {extracted}")
    print(f"⏱ Total Time: {elapsed:.2f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()
