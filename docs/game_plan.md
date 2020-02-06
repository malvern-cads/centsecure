# Game Plan

### General Tips
- Always make sure you kill the whole root of the problem
  e.g. Lets say you saw a netcat process, you wouldn't just stop the process, as that's not fixing the issue
  1. Look what runs the process (systemd or crontab for example)
  2. Is is a specific script?
  3. Are there any other related problems?
  4. Has it already done any damage?
  5. Can you reverse the damange?
  6. Are you confident the whole problem is gone?

### Windows

0. Preparation
    - Turn on hidden files and protected operating system ones
1. Forensics Questions
    - Try your absolute hardest before moving on
    - If struggling ask everyone around you for help
2. Operating System Updates
    - Get it started so it can run in the background
3. Autoruns
   - https://docs.microsoft.com/en-us/sysinternals/downloads/autoruns
   - Make sure it is run as Administrator
4. Centsecure
    - Centsecure will automate:
      - User Auditing
      - Local Policy
      - Account Policies
      - Group Policy
      - Defensive Counter Measure
    - Centsecure will aim to make sure the system is still usable after it is run
5. Installed Programs (? helped by centsecure)
    - Might be done by centsecure?
6. Service Auditing
    - Read through the extended service list
    - Make sure there are no anomalus items
    - Anything sounding dodgy should be stopped
7. Task manager check
    - Look through every process running in task manager
    - If it looks dodgy find the root of the problem
8. Application Updates
    - Try and update every application
    - The best shot sometimes is to reinstall the whole application rather than using the update within the application
9. Application Security Settings
    - Are all critical services secured to the max?
    - Is anything related to the critical service secure?
10. The Hunt  
    - Malicious Files
    - Unwanted software/hacking tools
    - User area nuke
      - Zip/backup all user areas
      - Delete all home folders that aren't the main user's
      
### GNU/Linux
1. Forensics Questions
    - Try your absolute hardest before moving on
    - If struggling ask everyone around you for help
2. Operating System Updates
    - Update OS
    - Set update settings accordingly
3. The Hunt 1.0
    - Crontab and other auto start
      - Check crontab and related files
      - Check systemd for start up services
    - Check systemd and services
      - Remove any dodgy services
    - Task Manager Check
      - Use `ps axjf`
      - Look for any backdoors or dodgy programs and remove the root of the problem
    - Port Scan
      - Make sure you run this as sudo
      - Look for any programs running on ports that aren't critical services
4. Centsecure
    - Centsecure will automate:
      - User Auditing
      - Local Policy
      - Account Policies
      - Defensive Counter Measure
    - Centsecure will aim to make sure the system is still usable after it is run
5. Remove Installed programs
    - Might not work until updates are finished
    - Note down any you come across but can't deal with at the time
6. Application Updates
    - Might have to wait for OS updates
7. Application Security Settings
    - Are all critical services secured to the max?
    - Is anything related to the critical service secure?
    - Make sure app updates don't overwrite changed configs
8. The Hunt 2.0
    - Malicious Files
    - User area nuke
      - Zip/backup all user areas
      - Delete all home folders that aren't the main user's
