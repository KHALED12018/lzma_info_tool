import lzma
import tkinter as tk
from tkinter import filedialog

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("LZMA Files", "*.lzma")])
    filepath_label.config(text="Selected file: " + filepath)
    global selected_file
    selected_file = filepath

def extract_info():
    if selected_file:
        with lzma.open(selected_file, 'rb') as f:
            header_bytes = f.read(13)
        
        uncompressed_size = int.from_bytes(header_bytes[1:5], byteorder='little')
        dictionary_size = int.from_bytes(header_bytes[5:9], byteorder='little')
        lc = header_bytes[9]
        lp = header_bytes[10]
        pb = header_bytes[11]
        
        result_text = f"{selected_file}\n"
        result_text += f"Uncompressed size: {uncompressed_size} bytes\n"
        result_text += f"Dictionary size: {dictionary_size} bytes\n"
        result_text += f"Literal context bits (lc): {lc}\n"
        result_text += f"Literal pos bits (lp): {lp}\n"
        result_text += f"Number of pos bits (pb): {pb}\n"
        
        result_label.config(text=result_text)
    else:
        result_label.config(text="No file selected!")

def apply_to_new_file():
    if selected_file:
        new_filepath = filedialog.asksaveasfilename(defaultextension=".lzma", filetypes=[("LZMA Files", "*")])
        if new_filepath:
            with lzma.open(new_filepath, 'wb') as new_f:
                properties = bytes([13])  # lzma1=dect...., lc=0, lp=2, pd=2
                dictionary_size = (2**23).to_bytes(4, byteorder='little')
                lc = b'\x00'
                lp = b'\x02'
                pb = b'\x02'
                header = properties + dictionary_size + lc + lp + pb
                new_f.write(header)
                
                with lzma.open(selected_file, 'rb') as f:
                    data = f.read()
                    new_f.write(data)
            
            apply_label.config(text="Applied settings to new file.")
        else:
            apply_label.config(text="No new file selected!")
    else:
        apply_label.config(text="No base file selected!")

selected_file = None

root = tk.Tk()
root.title("LZMA Info_By-DRAGON-NOIR")
root.geometry("600x650")

open_button = tk.Button(root, text="Open LZMA File", command=open_file)
open_button.pack(pady=10)

filepath_label = tk.Label(root, text="")
filepath_label.pack()

extract_button = tk.Button(root, text="Extract Info", command=extract_info)
extract_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack()

apply_button = tk.Button(root, text="Apply to New File", command=apply_to_new_file)
apply_button.pack(pady=10)

apply_label = tk.Label(root, text="")
apply_label.pack()

root.mainloop()
