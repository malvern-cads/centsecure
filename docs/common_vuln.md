# Common Vulnerabilities

This is a combined list of previous vulnerabilities from the list of previous vulnerabilities, so all of the Windows vulnerabilities have been put in a list and all of the Ubuntu/Debian vulnerabilities have been put in a list.

_The number in brackets is the number of points that you can expect to get from that vulnerability._

## Ubuntu/Debian
### Forensics Questions
- Forensics questions (6-10)
### User Auditing
- Created account as per brief (3-4)
- Guest account disabled (2-4)
- Removed unauthorized user, not in brief (2-4)
- Demoted user as per brief (4)
- Promoted user as per brief, to sudo (2-4)
- Changed insecure password (2-4)
- Created user (4)
### Account Policies
- Minimum password length is required (4)
- Default maximum password age set (3-4)
- Default minimum password age set (4)
- An account lockout policy is configured (4)
### Local Policies
### Defensive Counter Measure
- Firewall protection enabled (3-5)
### Service Auditing
- Software Installed/Started
    - sshd
    - Uncomplicated Firewall (UFW) protection has been enabled
- Software disabled/removed
    - Apache2 service
    - FTP
    - Samba service
    - SNMP service
### Operating System Updates
- The system automatically checks for updates daily (3-4)
- The system automatically checks for security updates (4)
- Installed important security updates (2-4)
### Application Updates
- Software updated
    - Bash updated (4)
    - Firefox updated (4)
    - Libre office updated (4)
    - Linux kernal has been updated (2)
    - OpenSSH updated (4)
    - OpenSSL shared libraries have been updated (2)
    - 7zip has been updated (3)
    - Pure FTP has been updated (3)
### Prohibited malware, prohibited files, unwanted software
- Prohibited Software/media removed
    - Removed plain text file containing passwords (4)
    - .mp3 files (5)
    - kismet removed (5)
    - ophcrack removed (5)
    - freeciv removed (5)
    - Kismet has been removed (3)
    - NMAP (and Zenmap) has been removed (3)
    - Freeciv has been removed (3)
    - Wireshark
    - Minetest
### uncategorized operating system settings    
- Stellarium has been installed (4)
- SSH root login disabled (4)
- Guest account is disabled (4)
- Removed netcat backdoor (5)
### Application Security Settings
- Firefox pop-up blocker enabled (5)


## Windows
### Forensics Questions
- Forensics questions (3-8)
### User Auditing
- Created user as per brief (3)
- Created group as per brief (4)
- Added users to new group as per brief (4)
- Removed unauthorized user (1-3)
- Guest account is not enabled (3)
- User is not an administrator (1-3)
- User has a password (1-3)
- Change insecure password (2-3)
- Create user (2)
- User password expires (3)
- User is an administrator (5)
### Account Policies
- Passwords must meet complexity requirements (3)
- A sufficient password history is being kept (5)
- A secure minimum password age exists (3)
- A secure minimum password length is required (3)
- A secure maximum password age is exists (2)
- A secure lockout threshold exists (2)
### Local Policies
- Audit Computer Account Management \[success\] (3)
- Audit Computer Account Management \[Failure\] (3)
- Audit Credential Validation \[Failure\] (5)
- Do not require CTRL+ALT+DEL \[disabled\] (10)
- Do not display last user name \[enabled\] (5)
- Limit local use of blank passwords to console only \[enabled\] (5)
- Users may not change system time (3)
- Switch to secure desktop when prompting for elavation \[enabled\] (3)
- A secure lockout threshold exists (2-3)
### Defensive Counter measures
- Firewall protection has been enabled (2-4)
- Anti virus protection has been enabled (4)
### Service Auditing
- Software disabled/stopped
    - ftp service (4)
    - Remote desktop sharing has been turned off (4)
    - Telnet service (4)
    - Simple TCP/IP services have been stopped and disabled (3)
    - UPnP Device host service has been stopped and disabled (3)
    - Net.TCP port sharing service has been stopped and disabled (3)
    - Remote registry service has been stopped and disabled (3)
    - File sharing disabled for C drive
    - World Wide Web Publishling service has been stopped and disabled *(Server only)*
### Operating System Updates
- Windows Update service is enabled - (5)
- The majority of windows updates have been installed (2-4)
- Windows automatically checks for updates (2-4)
### Application Updates
- Software updated
    - adobe reader dc has been updated (4)
    - firefox has been updated (3-4)
    - notepad++ updated (3)
    - Thunderbird has been updated (3)
    - Java has been updated (3)
    - Gimp has been updated (3)
    - PuTTY
### Prohibited malware, files unwanted software
- Removed prohibited software/media
    - .mp3 files (3)
    - removed Angry IP scanner
    - removed utorrent (3)
    - removed nmap (3)
    - removed kodi (3)
    - removed itunes (3)
    - removed teamviewer (3)
    - removed driver support (3)
    - removed Brutus password cracker archive(3)
    - removed angry ip scanner (3)
    - removed chicken invaders (3)
    - removed KNCTR (3)
    - removed bewear IRC server (3)
    - removed hashcat (3)
    - removed tini backdoor (3)
    - removed ophcrack
    - removed TightVNC Server (3)
    - removed BitTornado (2)
    - removed John the Ripper (2)
    - removed Advanced Port Scanner (2)
    - removed Real Player
    - removed Wireshark (3)
    - removed NetBus Pro
    - Removed netcat backdoor (4)
### Uncategorized Operating System Settings
- rdp network level authentication enabled (remote desktop) (4)
- Internet explorer has been installed (3)
- Internet explorer enhanced security configuration is enabled (3)
### Application Security SEttings
- Firefox warns when sites try to install add-ons (3)
- Firefox pop-up blocker enabled (5)
- Firefox blocks dangerous downloads (3)
- Firefox automatically checks for updates (3)
