#!/usr/bin/env python3
import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image

def shrink_pdf(input_file, output_file, pdf_quality='/ebook'):
    cmd = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS={pdf_quality}',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        f'-sOutputFile={output_file}',
        input_file
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"[INFO] Compressed PDF saved as: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to compress PDF '{input_file}': {e}")

def shrink_image(input_file, output_file, quality=75):
    try:
        img = Image.open(input_file)
        if img.format.lower() in ['jpeg', 'jpg']:
            img.save(output_file, format='JPEG', quality=quality, optimize=True)
        elif img.format.lower() == 'png':
            img.save(output_file, format='PNG', optimize=True)
        else:
            img.save(output_file, optimize=True)
        print(f"[INFO] Compressed image saved as: {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to compress image '{input_file}': {e}")

class PDFImageShrinkerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF & Image Shrinker")
        # Increase the size to ensure everything is visible
        self.geometry("650x720")
        self.configure(padx=10, pady=10)
        
        self.pdf_files = []
        self.img_files = []
        self.out_dir = ""
        
        self.create_widgets()
    
    def create_widgets(self):
        # --- Output Directory Section ---
        out_frame = tk.LabelFrame(self, text="Output Directory", padx=10, pady=10)
        out_frame.pack(fill="x", pady=5)
        
        self.out_dir_label = tk.Label(out_frame, text="Not selected (files will be saved in input folder)")
        self.out_dir_label.pack(side="left", padx=5)
        
        out_btn = tk.Button(out_frame, text="Set Output Directory", command=self.set_output_directory)
        out_btn.pack(side="right", padx=5)
        
        # --- PDF Files Section ---
        pdf_frame = tk.LabelFrame(self, text="PDF Files", padx=10, pady=10)
        pdf_frame.pack(fill="x", pady=5)
        
        pdf_list_frame = tk.Frame(pdf_frame)
        pdf_list_frame.pack(fill="x", expand=True)
        
        self.pdf_listbox = tk.Listbox(pdf_list_frame, height=5)
        self.pdf_listbox.pack(side="left", fill="both", expand=True)
        pdf_scrollbar = tk.Scrollbar(pdf_list_frame, orient="vertical", command=self.pdf_listbox.yview)
        pdf_scrollbar.pack(side="right", fill="y")
        self.pdf_listbox.config(yscrollcommand=pdf_scrollbar.set)
        
        # A separate frame for the "Add PDF Files" button
        pdf_btn_frame = tk.Frame(pdf_frame)
        pdf_btn_frame.pack(fill="x", pady=(5, 0))
        add_pdf_btn = tk.Button(pdf_btn_frame, text="Add PDF Files", command=self.add_pdf_files)
        add_pdf_btn.pack(side="left", padx=5)
        
        # PDF Compression Options
        pdf_opt_frame = tk.LabelFrame(self, text="PDF Compression Options", padx=10, pady=10)
        pdf_opt_frame.pack(fill="x", pady=5)
        
        tk.Label(pdf_opt_frame, text="PDF Quality (ghostscript setting):").pack(anchor="w")
        self.pdf_quality = tk.StringVar(value="/ebook")
        pdf_options = ["/screen", "/ebook", "/printer", "/prepress"]
        pdf_dropdown = ttk.Combobox(pdf_opt_frame, textvariable=self.pdf_quality,
                                    values=pdf_options, state="readonly")
        pdf_dropdown.pack(fill="x", padx=5, pady=2)
        
        # --- Image Files Section ---
        img_frame = tk.LabelFrame(self, text="Image Files", padx=10, pady=10)
        img_frame.pack(fill="x", pady=5)
        
        img_list_frame = tk.Frame(img_frame)
        img_list_frame.pack(fill="x", expand=True)
        
        self.img_listbox = tk.Listbox(img_list_frame, height=5)
        self.img_listbox.pack(side="left", fill="both", expand=True)
        img_scrollbar = tk.Scrollbar(img_list_frame, orient="vertical", command=self.img_listbox.yview)
        img_scrollbar.pack(side="right", fill="y")
        self.img_listbox.config(yscrollcommand=img_scrollbar.set)
        
        # A separate frame for the "Add Image Files" button
        img_btn_frame = tk.Frame(img_frame)
        img_btn_frame.pack(fill="x", pady=(5, 0))
        add_img_btn = tk.Button(img_btn_frame, text="Add Image Files", command=self.add_img_files)
        add_img_btn.pack(side="left", padx=5)
        
        # Image Compression Options
        img_opt_frame = tk.LabelFrame(self, text="Image Compression Options", padx=10, pady=10)
        img_opt_frame.pack(fill="x", pady=5)
        
        tk.Label(img_opt_frame, text="JPEG Quality (1-100):").pack(anchor="w")
        self.img_quality = tk.IntVar(value=75)
        img_scale = tk.Scale(img_opt_frame, from_=1, to=100, orient=tk.HORIZONTAL, variable=self.img_quality)
        img_scale.pack(fill="x", padx=5)
        
        # --- Run / Compress Button ---
        compress_btn = tk.Button(self, text="Shrink Files", command=self.shrink_files)
        compress_btn.pack(pady=20)
    
    def set_output_directory(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.out_dir = directory
            self.out_dir_label.config(text=f"Output Directory: {self.out_dir}")
        else:
            self.out_dir = ""
            self.out_dir_label.config(text="Not selected (files will be saved in input folder)")
    
    def add_pdf_files(self):
        selected = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if selected:
            for file in selected:
                if file not in self.pdf_files:
                    self.pdf_files.append(file)
                    self.pdf_listbox.insert(tk.END, file)
    
    def add_img_files(self):
        selected = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png"), ("All Files", "*.*")]
        )
        if selected:
            for file in selected:
                if file not in self.img_files:
                    self.img_files.append(file)
                    self.img_listbox.insert(tk.END, file)
    
    def shrink_files(self):
        if not self.pdf_files and not self.img_files:
            messagebox.showwarning("No Files Selected", "Please add PDF and/or image files before compressing.")
            return
        
        # Process PDF Files
        for file in self.pdf_files:
            if os.path.exists(file):
                base_name = os.path.splitext(os.path.basename(file))[0]
                out_path = self.out_dir if self.out_dir else os.path.dirname(file)
                output_file = os.path.join(out_path, f"{base_name}_shrunk.pdf")
                shrink_pdf(file, output_file, self.pdf_quality.get())
            else:
                print(f"[WARN] File does not exist: {file}")
        
        # Process Image Files
        for file in self.img_files:
            if os.path.exists(file):
                base_name, ext = os.path.splitext(os.path.basename(file))
                ext_lower = ext.lower()
                out_path = self.out_dir if self.out_dir else os.path.dirname(file)
                output_file = os.path.join(out_path, f"{base_name}_shrunk{ext_lower}")
                shrink_image(file, output_file, self.img_quality.get())
            else:
                print(f"[WARN] File does not exist: {file}")
        
        messagebox.showinfo("Process Completed", "All selected files have been processed. Check the console for details.")

if __name__ == "__main__":
    app = PDFImageShrinkerGUI()
    app.mainloop()

