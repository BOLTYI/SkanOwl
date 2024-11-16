# SkanOwl
A personnal cyber protection project

Here the discord community: https://discord.gg/hyb2869MWg

ScanOwl is a network scanning tool designed to detect known and unknown MAC addresses in a network environment. It allows users to manage and monitor network traffic in real-time, detect potential security issues like ARP spoofing and MAC spoofing, and provide insights into network activity.It aims to be usable on Windows and Linux. 

Features:
MAC Address Detection: Scans the network for MAC addresses, categorizing them as known or unknown based on user-defined files.
ARP Spoofing Detection: Identifies potential ARP spoofing attacks, where malicious devices try to impersonate other network devices. (In progress)
MAC Spoofing Detection: Detects if a device is spoofing its MAC address, which can be a sign of network security threats. (In progress)
File Management: Users can select and manage files containing known and unknown MAC addresses through a simple and intuitive PyQt5 interface. 
Real-Time Network Monitoring: The application continuously monitors network traffic and responds to detected security issues without interrupting the user interface.


Technologies Used:
Python: The core programming language used for network scanning and packet analysis.
Scapy: A powerful Python library used to capture and analyze network packets.
PyQt5: A framework for creating desktop applications with Python. It provides a graphical interface for users to interact with the tool.
Threading: Used to handle network packet sniffing in the background, allowing the interface to remain responsive during packet analysis. (In progress)


How It Works:
MAC Address File Selection: Users can select files containing known and unknown MAC addresses through the graphical interface.
Packet Sniffing: The tool continuously listens to network traffic to capture IP and MAC addresses.
Address Categorization: Captured MAC addresses are compared against the user’s files to determine whether they are known or unknown.
Security Threat Detection: The tool also detects ARP spoofing and MAC spoofing attacks, alerting the user if any suspicious activity is found. (In progress)


Future Improvements:
Enhanced User Interface: The tool is designed to evolve into a more user-friendly and feature-rich application with additional options for network monitoring and security. (priority)
Automated Threat Responses: Future versions will include automatic responses to detected threats, such as blocking malicious MAC addresses or alerting network administrators.
Advanced Network Metrics: The tool will evolve to track more network metrics, such as bandwidth usage, packet loss, and device behavior analysis.
Customizable Filters: Users will be able to set more advanced filtering rules for network traffic, improving the flexibility and accuracy of the scans.


Installation:
To install and run ScanOwl, make sure you have Python 3.x installed along with the required dependencies. Use the following steps to set up the environment:

Clone this repository to your local machine:
git clone https://github.com/yourusername/scanowl.git

Navigate to the project directory:
cd scanowl

Install the required libraries:
pip install scapy
pip install PyQT5


Run the application:
python interface.py

Contributing:
This project is open for contributions. If you would like to add features or fix bugs, feel free to fork the repository and submit a pull request.
Contributions can range from fixing issues to adding new functionalities, and all contributions are welcome.
The current priority is the GUI part.

License:
ScanOwl is licensed under the Apache 2.0 License.

ScanOwl is actively evolving and aims to become a comprehensive network monitoring and security tool. Stay tuned for more updates and features in future releases!
