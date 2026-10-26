from pathlib import Path
from pypdf import PdfReader, PdfWriter

INPUT_PDF = "output.pdf" # str(input("Enter pdf file name with .pdf at the end. eg : document.pdf"))
OUTPUT_FOLDER = "split_parts"

PAGES_PER_FILE = 100 # int(input("Enter number of pages you want per pdf. eg : 100"))  # Change this


def main():
    print("=" * 60)
    print("PDF SPLITTER (N Pages Per File)")
    print("=" * 60)

    input_path = Path(INPUT_PDF)

    if not input_path.exists():
        print(f"❌ File not found: {INPUT_PDF}")
        return

    output_dir = Path(OUTPUT_FOLDER)
    output_dir.mkdir(exist_ok=True)

    reader = PdfReader(INPUT_PDF)
    total_pages = len(reader.pages)

    print(f"📄 Input PDF : {INPUT_PDF}")
    print(f"📑 Total Pages: {total_pages}")
    print(f"📦 Pages/File : {PAGES_PER_FILE}")
    print()

    file_number = 1

    for start_page in range(0, total_pages, PAGES_PER_FILE):

        end_page = min(start_page + PAGES_PER_FILE, total_pages)

        print(
            f"Creating Part {file_number} "
            f"(Pages {start_page + 1}-{end_page})..."
        )

        writer = PdfWriter()

        for page in range(start_page, end_page):
            writer.add_page(reader.pages[page])

        output_file = output_dir / f"part_{file_number:03d}.pdf"

        with open(output_file, "wb") as f:
            writer.write(f)

        print(f"   ✅ Saved {output_file.name}")

        file_number += 1

    print("\n🎉 Splitting completed successfully!")
    print(f"📂 Output Folder: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
