Adversaries may abuse task scheduling functionality to facilitate initial or recurring execution of malicious code. Utilities exist within all major operating systems to schedule programs or scripts to be executed at a specified date and time.

#### T1053.002	At
```
core_user@coreserver:~$ sudo apt install at
```
Detection Logic
First install the necessary tools for logging (Note: this tool will be very noisy)
```
sudo apt-get install auditd audispd-plugins
sudo nano /etc/audit/rules.d/audit.rules

-a always,exit -F arch=b32 -S execve
-a always,exit -F arch=b64 -S execve

sudo systemctl enable auditd.service
sudo systemctl start auditd.service

sudo tail -f /var/log/audit/audit.log
```

logic
```
detection:
  condition: Selection_1
  Selection_1:
    audit_log|contains:
      - '"at"'
```


#### T1053.003	Cron
```
core_user@coreserver:~$ echo "echo 'hello'"> hello.sh
core_user@coreserver:~$ crontab -e
*/2 * * * * sh /home/core_user/hello.sh
# this will be executed every 2 minutes
```
Detection Logic
```
detection:
  condition: Selection_1
  Selection_1:
    Process|all:
      - crontab
    EventData|contains:
      - 'REPLACE '
```

#### T1053.005	Scheduled Task

Adversaries may also create "hidden" scheduled tasks (i.e. Hide Artifacts) that may not be visible to defender tools and manual queries used to enumerate tasks. Specifically, an adversary may hide a task from schtasks /query and the Task Scheduler by deleting the associated Security Descriptor (SD) registry value (where deletion of this value must be completed using SYSTEM permissions). Adversaries may also employ alternate methods to hide tasks, such as altering the metadata (e.g., Index value) within associated registry keys.

Detection Logic
```
//creation
detection:
  condition: win_event
  win_event:
    Channel|all:
      - Microsoft-Windows-TaskScheduler/Operational
    EventID|all:
      - '106'

//deletion
detection:
  condition: win_event
  win_event:
    Channel|all:
      - Microsoft-Windows-TaskScheduler/Operational
    EventID|all:
      - '141'
```

TODO: create a script to do the below API commands: 
ref: https://hadess.io/the-art-of-windows-persistence/
```
schtasks /query /tn "EXISTING_TASK" /xml > out.xml
# now modify the <Principals> section in xml file with <RunLevel>HighestAvailable</RunLevel>
# now delete the orginal task and replace it with modified version
schtasks /delete /tn "EXISTING_TASK" /f
schtasks /create /tn "EXISTING_TASK" /xml out.xml
```

#### T1053.006	Systemd Timers
#### T1053.007	Container Orchestration Job