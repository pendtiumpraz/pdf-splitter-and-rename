import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter

class ModernEntry(ttk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(style='Modern.TEntry')

class PDFToolsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengolah PDF")
        
        # Configure window
        self.root.state('zoomed')
        self.root.minsize(800, 600)
        
        # Set theme and style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('TNotebook', background='#f5f5f5')
        style.configure('TFrame', background='#ffffff')
        style.configure('TLabel', background='#ffffff', font=('Segoe UI', 10))
        
        # Modern Entry Style
        style.configure('Modern.TEntry',
            padding=10,
            relief='flat',
            font=('Segoe UI', 10)
        )
        
        # Header styles
        style.configure('Header.TLabel',
            font=('Segoe UI', 24, 'bold'),
            padding=20,
            foreground='#2c3e50'
        )
        style.configure('Subheader.TLabel',
            font=('Segoe UI', 12),
            padding=10,
            foreground='#34495e'
        )
        
        # Main container with padding
        main_container = ttk.Frame(root)
        main_container.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill='x', pady=(0, 30))
        ttk.Label(header_frame, text="Aplikasi Pengolah PDF", style='Header.TLabel').pack()
        ttk.Label(header_frame, text="Pilih menu di bawah untuk memulai", style='Subheader.TLabel').pack()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Create tabs
        self.split_tab = ttk.Frame(self.notebook)
        self.rename_tab = ttk.Frame(self.notebook)
        self.help_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.split_tab, text='Pemecah PDF')
        self.notebook.add(self.rename_tab, text='Pengubah Nama PDF')
        self.notebook.add(self.help_tab, text='Bantuan')
        
        self.setup_split_tab()
        self.setup_rename_tab()
        self.setup_help_tab()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Bind escape key to toggle full screen
        self.root.bind('<Escape>', self.toggle_fullscreen)
        
        # Store fullscreen state
        self.fullscreen = True

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.state('zoomed' if self.fullscreen else 'normal')

    def on_closing(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar?"):
            self.root.destroy()

    def create_input_group(self, parent, label_text, entry_var, browse_command=None, width=50):
        frame = ttk.Frame(parent)
        frame.pack(fill='x', pady=10)
        
        label = ttk.Label(frame, text=label_text, style='Subheader.TLabel')
        label.pack(anchor='w', pady=(0, 5))
        
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill='x')
        
        entry = ModernEntry(input_frame, textvariable=entry_var, width=width)
        entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        if browse_command:
            browse_btn = tk.Button(input_frame, text="Pilih", command=browse_command,
                               bg='#007bff', fg='white', font=('Segoe UI', 10),
                               padx=20, pady=5)
            browse_btn.pack(side='right')
        
        return frame

    def setup_help_tab(self):
        container = ttk.Frame(self.help_tab)
        container.pack(expand=True, fill='both', padx=40, pady=30)
        
        # Title
        ttk.Label(container, text="Petunjuk Penggunaan", 
                 style='Header.TLabel').pack(pady=(0, 30))
        
        # Split PDF Instructions
        split_frame = ttk.Frame(container)
        split_frame.pack(fill='x', pady=10)
        ttk.Label(split_frame, text="Pemecah PDF", 
                 font=('Segoe UI', 14, 'bold')).pack(anchor='w')
        split_instructions = """
        1. Pilih file PDF yang ingin dipecah
        2. Tentukan folder untuk menyimpan hasil
        3. Masukkan jumlah halaman yang diinginkan per file
        4. Klik tombol 'Mulai Memecah PDF'
        """
        ttk.Label(split_frame, text=split_instructions, 
                 style='Subheader.TLabel', justify='left').pack(pady=10)
        
        # Rename PDF Instructions
        rename_frame = ttk.Frame(container)
        rename_frame.pack(fill='x', pady=20)
        ttk.Label(rename_frame, text="Pengubah Nama PDF", 
                 font=('Segoe UI', 14, 'bold')).pack(anchor='w')
        rename_instructions = """
        1. Pilih folder yang berisi file PDF yang akan diubah namanya
        2. Pilih file CSV/Excel yang berisi daftar nama baru
        3. Masukkan awalan dan akhiran untuk format nama file
        4. Klik tombol 'Mulai Mengubah Nama'
        
        Format nama file: [Awalan]_[Nama]_[Akhiran].pdf
        """
        ttk.Label(rename_frame, text=rename_instructions, 
                 style='Subheader.TLabel', justify='left').pack(pady=10)

    def setup_split_tab(self):
        container = ttk.Frame(self.split_tab)
        container.pack(expand=True, fill='both', padx=40, pady=30)
        
        # Title
        ttk.Label(container, text="Pemecah File PDF", 
                 style='Header.TLabel').pack(pady=(0, 30))
        
        # Input fields
        self.input_pdf_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.pages_per_split = tk.StringVar(value="8")
        
        self.create_input_group(container, "File PDF yang akan dipecah:", 
                              self.input_pdf_path, self.browse_input_pdf)
        self.create_input_group(container, "Folder untuk menyimpan hasil:", 
                              self.output_folder, self.browse_output_folder)
        self.create_input_group(container, "Jumlah halaman per file:", 
                              self.pages_per_split, width=10)
        
        # Split button
        split_button = tk.Button(
            container,
            text="Mulai Memecah PDF",
            command=self.split_pdf,
            bg='#28a745',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            padx=30,
            pady=15,
            cursor='hand2'
        )
        split_button.pack(pady=30, padx=50, fill='x')

    def setup_rename_tab(self):
        container = ttk.Frame(self.rename_tab)
        container.pack(expand=True, fill='both', padx=40, pady=30)
        
        # Title
        ttk.Label(container, text="Pengubah Nama File PDF", 
                 style='Header.TLabel').pack(pady=(0, 30))
        
        # Input fields
        self.pdf_folder = tk.StringVar()
        self.name_file = tk.StringVar()
        self.output_prefix = tk.StringVar()
        self.suffix = tk.StringVar()
        
        self.create_input_group(container, "Folder yang berisi file PDF:", 
                              self.pdf_folder, self.browse_pdf_folder)
        self.create_input_group(container, "File daftar nama (CSV/Excel):", 
                              self.name_file, self.browse_name_file)
        self.create_input_group(container, "Awalan nama file:", 
                              self.output_prefix)
        self.create_input_group(container, "Akhiran nama file:", 
                              self.suffix)
        
        # Rename button
        rename_button = tk.Button(
            container,
            text="Mulai Mengubah Nama",
            command=self.rename_pdfs,
            bg='#28a745',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            padx=30,
            pady=15,
            cursor='hand2'
        )
        rename_button.pack(pady=30, padx=50, fill='x')

    def browse_input_pdf(self):
        try:
            filename = filedialog.askopenfilename(filetypes=[("File PDF", "*.pdf")])
            if filename:
                self.input_pdf_path.set(filename)
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Terjadi kesalahan saat memilih file: {str(e)}")

    def browse_output_folder(self):
        try:
            folder = filedialog.askdirectory()
            if folder:
                self.output_folder.set(folder)
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Terjadi kesalahan saat memilih folder: {str(e)}")

    def browse_pdf_folder(self):
        try:
            folder = filedialog.askdirectory()
            if folder:
                self.pdf_folder.set(folder)
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Terjadi kesalahan saat memilih folder: {str(e)}")

    def browse_name_file(self):
        try:
            filename = filedialog.askopenfilename(filetypes=[
                ("File CSV", "*.csv"),
                ("File Excel", "*.xlsx;*.xls")
            ])
            if filename:
                self.name_file.set(filename)
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Terjadi kesalahan saat memilih file: {str(e)}")

    def split_pdf(self):
        try:
            input_path = self.input_pdf_path.get()
            output_folder = self.output_folder.get()
            try:
                pages_per_split = int(self.pages_per_split.get())
            except ValueError:
                messagebox.showerror("Kesalahan", "Jumlah halaman harus berupa angka")
                return

            if not input_path or not output_folder:
                messagebox.showerror("Kesalahan", "Mohon lengkapi semua field yang diperlukan")
                return

            if not os.path.exists(input_path):
                messagebox.showerror("Kesalahan", f"File '{input_path}' tidak ditemukan")
                return

            reader = PdfReader(input_path)
            total_pages = len(reader.pages)
            os.makedirs(output_folder, exist_ok=True)

            for i in range(0, total_pages, pages_per_split):
                writer = PdfWriter()
                for j in range(i, min(i + pages_per_split, total_pages)):
                    writer.add_page(reader.pages[j])

                output_filename = os.path.join(output_folder, f"part_{i // pages_per_split + 1:02}.pdf")
                with open(output_filename, "wb") as output_pdf:
                    writer.write(output_pdf)

            messagebox.showinfo("Berhasil", 
                f"Pemecahan PDF selesai!\nTotal bagian: {total_pages // pages_per_split + (1 if total_pages % pages_per_split else 0)}\n"
                f"Hasil disimpan di: '{output_folder}'")
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Terjadi kesalahan: {str(e)}")

    def rename_pdfs(self):
        try:
            folder_path = self.pdf_folder.get()
            name_file_path = self.name_file.get()
            output_prefix = self.output_prefix.get()
            suffix = self.suffix.get()

            if not all([folder_path, name_file_path, output_prefix, suffix]):
                messagebox.showerror("Kesalahan", "Mohon lengkapi semua field yang diperlukan")
                return

            # Read names from CSV or Excel
            if name_file_path.endswith('.csv'):
                names = pd.read_csv(name_file_path, header=None)
            else:
                names = pd.read_excel(name_file_path)

            # Get first column as list of names
            name_list = names.iloc[:, 0].tolist()

            # Find all files starting with part_ and sort them
            pdf_files = sorted([f for f in os.listdir(folder_path) if f.startswith("part_") and f.endswith(".pdf")])

            if len(pdf_files) != len(name_list):
                messagebox.showerror("Kesalahan", 
                    f"Jumlah file PDF ({len(pdf_files)}) tidak sama dengan jumlah nama ({len(name_list)})")
                return

            for old_name, new_name in zip(pdf_files, name_list):
                old_path = os.path.join(folder_path, old_name)
                sanitized_name = new_name.strip().replace(" ", "_")
                new_filename = f"{output_prefix}_{sanitized_name}_{suffix}.pdf"
                new_path = os.path.join(folder_path, new_filename)
                os.rename(old_path, new_path)

            messagebox.showinfo("Berhasil", "Pengubahan nama selesai. Semua file telah diubah namanya.")
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = PDFToolsApp(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}") 