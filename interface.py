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
            # Assuming you want to call the scan function
            host_ip = module.get_host_ip()  # Get the host_ip from netscan.py
            if host_ip:
                result = module.scan(host_ip)
                self.display_result(result)
                module.scanDevices(result)
            else:
                print("Failed to get host IP.")
        else:
            print(f"Error: {module_file_path} does not exist.")

    def display_result(self, result):
        self.text_area.delete(1.0, tk.END)  # Clear existing content
        self.log("Scan Results:")
        for item in result:
            self.log(f"IP: {item['ip']}, MAC: {item['mac']}, Hostname: {item['hostname']}")
            open_ports = item.get('open_ports', [])
            if open_ports:
                self.log(f"Open ports for {item['ip']}: {', '.join(map(str, open_ports))}")
            else:
                self.log(f"No open ports found for {item['ip']}")
            self.log("-" * 50)

    def log(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetScanGUI(root)
    root.mainloop()
