import os
import pandas as pd

def rename_pdfs(folder_path, name_file_path, output_prefix, suffix):
    # Membaca nama dari CSV atau Excel
    if name_file_path.endswith('.csv'):
        names = pd.read_csv(name_file_path, header=None)  # Perhatikan bagian ini!
    else:
        names = pd.read_excel(name_file_path)

    # Ambil hanya kolom pertama sebagai list nama
    name_list = names.iloc[:, 0].tolist()

    # Cari semua file dengan awalan part_ dan urutkan
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.startswith("part_") and f.endswith(".pdf")])

    if len(pdf_files) != len(name_list):
        print(f"Jumlah file PDF ({len(pdf_files)}) tidak sama dengan jumlah nama ({len(name_list)}).")
        return

    for old_name, new_name in zip(pdf_files, name_list):
        old_path = os.path.join(folder_path, old_name)
        sanitized_name = new_name.strip().replace(" ", "_")
        new_filename = f"{output_prefix}_{sanitized_name}_{suffix}.pdf"
        new_path = os.path.join(folder_path, new_filename)
        os.rename(old_path, new_path)

    print("Renaming complete. Semua file telah diberi nama baru.")

if __name__ == "__main__":
    folder_path = input("Masukkan folder yang berisi file PDF: ").strip()
    name_file_path = input("Masukkan path ke file CSV/Excel (nama): ").strip()
    output_prefix = input("Masukkan prefix nama file (misal: Progress_Report): ").strip()
    suffix = input("Masukkan suffix nama file (misal: Coding1st_Maret_2025): ").strip()

    rename_pdfs(folder_path, name_file_path, output_prefix, suffix)
