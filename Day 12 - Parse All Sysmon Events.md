So far we have added parsing for sysmon event id 1 and 8. Now let's convert all other events. 


Status      |ID	|Tag    |Event
---------   |----|-------|------
Completed   |1	|ProcessCreate|	Process Create
Pending     |2	|FileCreateTime|	File creation time
Pending     |3	|NetworkConnect|	Network connection detected
Pending     |4	|n/a|	Sysmon service state change (cannot be filtered)
Pending     |5	|ProcessTerminate|	Process terminated
Pending     |6	|DriverLoad|	Driver Loaded
Pending     |7	|ImageLoad|	Image loaded
Completed     |8	|CreateRemoteThread|	CreateRemoteThread detected
Pending     |9	|RawAccessRead|	RawAccessRead detected
Pending     |10	|ProcessAccess|	Process accessed
Pending     |11	|FileCreate|	File created
Pending     |12	|RegistryEvent|	Registry object added or deleted
Pending     |13	|RegistryEvent|	Registry value set
Pending     |14	|RegistryEvent|	Registry object renamed
Pending     |15	|FileCreateStreamHash|	File stream created
Pending     |16	|n/a|	Sysmon configuration change (cannot be filtered)
Pending     |17	|PipeEvent|	Named pipe created
Pending     |18	|PipeEvent|	Named pipe connected
Pending     |19	|WmiEvent|	WMI filter
Pending     |20	|WmiEvent|	WMI consumer
Pending     |21	|WmiEvent|	WMI consumer filter
Pending     |22	|DNSQuery|	DNS query
Pending     |23	|FileDelete|	File Delete archived
Pending     |24	|ClipboardChange|	New content in the clipboard
Pending     |25	|ProcessTampering|	Process image change
Pending     |26	|FileDeleteDetected|	File Delete logged
Pending     |27	|FileBlockExecutable|	File Block Executable
Pending     |28	|FileBlockShredding|	File Block Shredding
Pending     |29	|FileExecutableDetected|	File Executable Detected

