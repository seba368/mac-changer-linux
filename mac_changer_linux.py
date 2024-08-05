#!/usr/bin/env python3

import argparse
import re
import subprocess
from typing import Optional


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Change MAC address")
    parser.add_argument("-i", "--interface", dest="interface", required=True,
                        help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", required=True, help="New MAC address")
    return parser.parse_args()


def change_mac(interface: str, new_mac: str) -> None:
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    try:
        subprocess.check_call(["ifconfig", interface, "down"])
        subprocess.check_call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.check_call(["ifconfig", interface, "up"])
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to change MAC address: {e}")


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


def main():
    options = get_arguments()
    current_mac = get_current_mac(options.interface)
    if current_mac:
        print(f"Current MAC = {current_mac}")

    change_mac(options.interface, options.new_mac)
    current_mac = get_current_mac(options.interface)

    if current_mac == options.new_mac:
        print(f"[+] MAC address was successfully changed to {current_mac}")
    else:
        print("[-] MAC address did not get changed.")


if __name__ == "__main__":
    main()
