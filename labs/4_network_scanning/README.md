Let 4: Network Pentest
======================

👒Background👒
---------------
You have just been hired by Hattitude: a brand new company who is looking to disrupt the hat-wearing industry with their lean agile methodology and novel web-based value proposition! They are days away from launching their new website, and want to make sure that it is completely safe and secure.

Hattitude has spared no expense, and they have hired 249 of the best security experts to test their network. This is where you come in! You will be given access to their internal network, as if you were a brand new employee. You will need to find any flaws in their security, and write a report to their CEO detailing your findings.

🎓Instructions🎓
----------------
You will be given VPN access to Hattitude’s internal network, and you are allowed to access any device in their private IP range: 172.16.10.0 through 172.16.10.255

Scope (Important!)
------------------
It is very important that you only inspect sites in the given range! Anything outside of that range is not part of this assignment. Additionally, you can steal credentials, log in as any employee, and read any data you can find, but you must not modify files or cause damage to their systems. Intentionally damaging the environment will result in a zero on the assignment.

### Connecting to the VPN
Hattitude employees use the OpenVPN program to connect to the company network. You can connect to their VPN with these steps:
- Download the OpenVPN client from https://openvpn.net/vpn-client/.
- Download the VPN configuration file from the “midterm” link on https://csci3403.com.
- Open the OpenVPN client and import the configuration file you just downloaded.

### Downloading nmap
You will need to start by using nmap to scan the IP range and see which devices are running. You can download nmap from https://nmap.org/download (Windows installer, Mac installer).

Scoring
-------
Your goal is to collect various secrets hidden around the network called flags, which represent sensitive information like passwords or private keys. Each flag will be in the same recognizable format of {flag#-_____}, for example: {flag0-3xampl3}. A hint for each flag is in the Flags section below.

Each flag is worth 20% of your grade. There are six flags hidden around the network, but you only need five to get full points. The last one will be extra credit. You will submit the flags and the writeup on Canvas.

🎩Flags🎩
----------
### Flag #1: Exposed Credentials
See if your client has left any important credentials sitting around in any scripts or internal documentation which is accessible from anyone on the private network.
### Flag #2: CCTV Cameras
Your clients use CCTV cameras to monitor their office. See if the cameras have captured any lapses in their developer’s physical security.
### Flag #3: Unencrypted Login
Alice, the head of IT, uses TELNET to log in to one of the production servers. Steal her password. You will need to run a packet capture on the TELNET server itself, which may require finding a set of lower level credentials first. Note: You can create a .pcap file for this portion, but please delete it when you’re finished. We will automatically delete .pcap files after a few minutes.
### Flag #4: Private Keys
See if any developers have created private SSH keys which you could read.
### Flag #5: Database
See if you can read any important information out of the database. If you haven’t worked with PostgreSQL before, the company’s internal documentation might have some tips to get started.
### Flag #6: Password Cracking
Carol’s password is one of the 100 most common passwords. The flag is in her home directory.