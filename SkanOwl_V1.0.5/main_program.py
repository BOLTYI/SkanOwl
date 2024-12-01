from PyQt5.QtWidgets import QFileDialog
from scapy.all import sniff
from scapy.layers.inet import IP, Ether
from scapy.layers.l2 import ARP
import threading
import os

# Global variables for file paths
known_mac_file = ""  # Path to the file of known MAC addresses
unknown_mac_file = ""  # Path to the file of unknown MAC addresses

# Variable to control program execution
running = True
monitoring_running = False  # To track if network monitoring is running
monitoring_event = threading.Event()  # Event to control thread termination
monitoring_threads = []  # To store monitoring threads

# For storing previously detected MAC addresses to avoid redundant logs
known_macs_set = set()
unknown_macs_set = set()

# Function to start MAC acquisition
def start_mac_acquisition_thread():
    """Start MAC address acquisition thread."""
    global monitoring_event
    print("[*] Starting MAC address acquisition thread...\n")
    monitoring_event.clear()  # Ensure the event is cleared before starting
    thread = threading.Thread(target=run_program)
    thread.daemon = True  # Allow thread to exit when the program ends
    thread.start()

def stop_all_threads():
    """Stop the program and all threads."""
    global running, monitoring_event
    running = False
    monitoring_event.set()  # Signal all threads to stop
    print("[*] Stopping all threads...\n")

def controlled_sniff(filter, prn, store=0, timeout=1):
    """
    Sniff packets with the ability to stop using the monitoring_event.
    """
    while not monitoring_event.is_set():
        sniff(filter=filter, prn=prn, store=store, timeout=timeout)

def start_network_monitoring_threads():
    """Start or stop threads for network monitoring."""
    global monitoring_running, monitoring_event, monitoring_threads

    if monitoring_running:
        print("[*] Network monitoring is already running. Stopping...\n")
        stop_network_monitoring()
    else:
        print("[*] Starting network monitoring threads...\n")
        monitoring_running = True
        monitoring_event.clear()  # Reset the event

        # Creating threads for network monitoring tasks
        threads = []

        # Thread for MAC comparison
        mac_thread = threading.Thread(target=controlled_sniff, kwargs={
            "filter": "ip",
            "prn": compare_src_mac_with_known_mac_file
        })
        threads.append(mac_thread)

        # Thread for ARP spoofing detection
        arp_thread = threading.Thread(target=controlled_sniff, kwargs={
            "filter": "arp",
            "prn": detect_arp_spoofing
        })
        threads.append(arp_thread)

        # Thread for MAC spoofing detection
        spoofing_thread = threading.Thread(target=controlled_sniff, kwargs={
            "filter": "arp",
            "prn": detect_mac_spoofing
        })
        threads.append(spoofing_thread)

        # Start all threads
        for thread in threads:
            thread.start()

        monitoring_threads = threads

def stop_network_monitoring():
    """Stop the network monitoring threads."""
    global monitoring_running, monitoring_event, monitoring_threads

    monitoring_event.set()  # Signal the threads to stop
    monitoring_running = False
    print("[*] Stopping network monitoring...\n")

    for thread in monitoring_threads:
        if thread.is_alive():
            thread.join()

    monitoring_threads.clear()
    print("[*] All monitoring threads stopped.\n")

def select_known_mac(file_path):
    """Set the file for known MAC addresses."""
    global known_mac_file, known_macs_set

    if os.path.exists(file_path):
        known_mac_file = file_path
        print(f"[+] Selected known MAC file: {known_mac_file}\n")

        # Load existing MAC addresses into the set
        try:
            with open(known_mac_file, "r") as file:
                known_macs_set.update(line.strip() for line in file)
            print(f"[+] Loaded {len(known_macs_set)} MAC addresses from the file.\n")
        except Exception as e:
            print(f"[!] Error reading known MAC file: {e}\n")
    else:
        print("[!] The selected file does not exist.\n")

def select_unknown_mac(file_path):
    """Set the file for unknown MAC addresses."""
    global unknown_mac_file

    if os.path.exists(file_path):
        unknown_mac_file = file_path
        print(f"[+] Selected unknown MAC file: {unknown_mac_file}\n")
    else:
        print("[!] The selected file does not exist.\n")

def compare_src_mac_with_known_mac_file(pkt):
    """Compare source MAC addresses with known addresses."""
    global known_mac_file, unknown_mac_file, known_macs_set, unknown_macs_set

    if pkt.haslayer(IP) and pkt.haslayer(Ether):
        src_ip = pkt[IP].src
        src_mac = pkt[Ether].src

        if src_mac in known_macs_set:
            print(f"[+] Known MAC address detected: {src_mac} (IP: {src_ip})\n")
        else:
            if unknown_mac_file and src_mac not in unknown_macs_set:
                try:
                    with open(unknown_mac_file, "a") as file:
                        file.write(f"{src_mac}\n")
                    unknown_macs_set.add(src_mac)
                    print(f"[*] Added unknown MAC address: {src_mac}\n")
                except Exception as e:
                    print(f"[!] Error writing to unknown MAC file: {e}\n")
            else:
                print(f"[!] Unknown MAC address already logged: {src_mac}\n")

def write_mac_to_sd(pkt):
    """Write captured MAC addresses to the known MAC file."""
    global known_mac_file, known_macs_set

    if not known_mac_file:
        print("[!] Known MAC file not set. Please select a file first.\n")
        return

    if pkt.haslayer(Ether):
        src_mac = pkt[Ether].src

        if src_mac not in known_macs_set:
            try:
                with open(known_mac_file, "a") as file:
                    file.write(f"{src_mac}\n")
                known_macs_set.add(src_mac)
                print(f"[+] MAC address written to file: {src_mac}\n")
            except Exception as e:
                print(f"[!] Error writing to file: {e}\n")
        else:
            print(f"[*] MAC address already exists: {src_mac}\n")

def detect_arp_spoofing(pkt):
    """Detect ARP spoofing attempts."""
    if pkt.haslayer(ARP) and pkt[ARP].op == 2:  # ARP reply
        source_ip = pkt[ARP].psrc
        source_mac = pkt[ARP].hwsrc
        print(f"[!] ARP Spoofing Check: IP={source_ip}, MAC={source_mac}\n")

def detect_mac_spoofing(pkt):
    """Detect MAC spoofing."""
    if pkt.haslayer(Ether) and pkt.haslayer(ARP):
        ethernet_mac = pkt[Ether].src
        arp_mac = pkt[ARP].hwsrc

        if ethernet_mac != arp_mac:
            print(f"[!] MAC Spoofing detected! Ethernet MAC: {ethernet_mac}, ARP MAC: {arp_mac}\n")

def run_program():
    """Start capturing packets for MAC address acquisition."""
    global running
    running = True
    print("[*] Starting MAC address acquisition...\n")
    controlled_sniff(filter="ip", prn=write_mac_to_sd)
