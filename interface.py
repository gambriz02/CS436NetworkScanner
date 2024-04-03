import tkinter as tk
from tkinter import scrolledtext
import threading
import socket
import os
import importlib.util

class NetScanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Scanner")

        self.text_area = scrolledtext.ScrolledText(root, width=80, height=20)
        self.text_area.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Scan", command=self.start_scan)
        self.start_button.pack(pady=5)

    def start_scan(self):
        module_name = 'netscan'
        module_file_path = f'{module_name}.py'
        if os.path.exists(module_file_path):
            spec = importlib.util.spec_from_file_location(module_name, module_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Assuming you want to call the main function
            module.main()
        else:
            print(f"Error: {module_file_path} does not exist.")

    def log(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetScanGUI(root)
    root.mainloop()
