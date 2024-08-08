#!/usr/bin/env python3

import re
import subprocess
import tkinter as tk
from tkinter import messagebox
from typing import Optional


def change_mac(interface: str, new_mac: str) -> None:
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    try:
        subprocess.check_call(["ifconfig", interface, "down"])
        subprocess.check_call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.check_call(["ifconfig", interface, "up"])
        messagebox.showinfo("Success", f"MAC address was successfully changed to {new_mac}")
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to change MAC address: {e}")
        messagebox.showerror("Error", f"Failed to change MAC address: {e}")


def get_current_mac(interface: str) -> Optional[str]:
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()
        mac_address_search_result = re.search(r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", ifconfig_result)
        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            print("[-] Could not read MAC address.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"[-] Could not execute ifconfig: {e}")
        return None
    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")
        return None


def on_change_mac():
    interface = interface_entry.get()
    new_mac = mac_entry.get()
    if not interface or not new_mac:
        messagebox.showwarning("Input Error", "Please provide both interface and new MAC address")
        return

    current_mac = get_current_mac(interface)
    if current_mac:
        print(f"Current MAC = {current_mac}")
    change_mac(interface, new_mac)
    current_mac = get_current_mac(interface)
    if current_mac == new_mac:
        print(f"[+] MAC address was successfully changed to {current_mac}")
    else:
        print("[-] MAC address did not get changed.")
        messagebox.showerror("Error", "MAC address did not get changed.")


# Create the main window
root = tk.Tk()
root.title("MAC Address Changer")

# Create and place the interface label and entry
tk.Label(root, text="Interface:").grid(row=0, column=0, padx=10, pady=10)
interface_entry = tk.Entry(root)
interface_entry.grid(row=0, column=1, padx=10, pady=10)

# Create and place the MAC address label and entry
tk.Label(root, text="New MAC Address:").grid(row=1, column=0, padx=10, pady=10)
mac_entry = tk.Entry(root)
mac_entry.grid(row=1, column=1, padx=10, pady=10)

# Create and place the Change MAC button
change_mac_button = tk.Button(root, text="Change MAC", command=on_change_mac)
change_mac_button.grid(row=2, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()
