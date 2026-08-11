import time
from pathlib import Path
from pypdf import PdfReader, PdfWriter

# ==================================================
# Configuration
# ==================================================

INPUT_PDF = str(input("Enter the pdf name with .pdf at the end. Eg : document.pdf : "))
OUTPUT_PDF = "output.pdf"

PAGES_TO_DELETE = int(input("Enter number of pages you want to delete from the start : "))

# ==================================================


def main():

    start = time.time()

    print("=" * 60)
    print("DELETE FIRST N PAGES FROM PDF")
    print("=" * 60)

    input_path = Path(INPUT_PDF)

    if not input_path.exists():
        print(f"❌ File not found: {INPUT_PDF}")
        return

    print(f"📄 Reading: {INPUT_PDF}")

    reader = PdfReader(INPUT_PDF)
    total_pages = len(reader.pages)

    print(f"✅ Total Pages: {total_pages}")
    print(f"🗑 Pages to Delete: {PAGES_TO_DELETE}")

    if PAGES_TO_DELETE >= total_pages:
        print("❌ Cannot delete all pages. Reduce PAGES_TO_DELETE.")
        return

    writer = PdfWriter()

    remaining = total_pages - PAGES_TO_DELETE

    print(f"\n✂ Keeping {remaining} pages...\n")

    for page_number in range(PAGES_TO_DELETE, total_pages):

        writer.add_page(reader.pages[page_number])

        print(
            f"✅ Added page {page_number + 1}/{total_pages}",
            flush=True
        )

    print("\n💾 Saving output PDF...")

    with open(OUTPUT_PDF, "wb") as output_file:
        writer.write(output_file)

    elapsed = time.time() - start

    print(f"✅ Saved: {OUTPUT_PDF}")
    print(f"⏱ Total Time: {elapsed:.2f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()
