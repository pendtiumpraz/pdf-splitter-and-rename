import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path, output_folder, pages_per_split=8):
    if not os.path.exists(input_pdf_path):
        print(f"File '{input_pdf_path}' tidak ditemukan.")
        return

    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    os.makedirs(output_folder, exist_ok=True)

    for i in range(0, total_pages, pages_per_split):
        writer = PdfWriter()
        for j in range(i, min(i + pages_per_split, total_pages)):
            writer.add_page(reader.pages[j])

        output_filename = os.path.join(output_folder, f"part_{i // pages_per_split + 1:02}.pdf")
        with open(output_filename, "wb") as output_pdf:
            writer.write(output_pdf)

    print(f"PDF split complete! Total parts: {total_pages // pages_per_split + (1 if total_pages % pages_per_split else 0)}")
    print(f"Hasil disimpan di folder: '{output_folder}'")

if __name__ == "__main__":
    input_pdf_path = input("Masukkan path ke file PDF: ").strip()
    output_folder = input("Masukkan nama folder output: ").strip()
    split_pdf(input_pdf_path, output_folder)
