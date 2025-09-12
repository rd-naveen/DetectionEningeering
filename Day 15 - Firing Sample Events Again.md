For this we need to save the json events in a separate file and use the Source tail plugin to read the logs, parse and send it to the remote index.

<source>
  @type tail
  path /home/core_user/samples.txt
  tag winevt.raw
  read_from_head true
  <parse>
    @type json
  </parse>
</source>

Sample events in the file (Note: each event in a new line)
```
{"ProviderName":"Microsoft-Windows-Sysmon","ProviderGUID":"","EventID":"2","Level":"4","Task":"2","Opcode":"0","Keywords":"0x8000000000000000","TimeCreated":"2025/09/07 07:37:43.913943200","EventRecordID":"29124","ActivityID":"","RelatedActivityID":"","ProcessID":"3544","ThreadID":"4200","Channel":"Microsoft-Windows-Sysmon/Operational","Computer":"DESKTOP-K05T3EJ","UserID":"S-1-5-18","User":"NT AUTHORITY\\SYSTEM","Version":"5","Description":"File creation time changed:\r\nRuleName: T1099\r\nUtcTime: 2025-09-07 07:37:43.913\r\nProcessGuid: {b2a55edd-95d0-68b5-7a07-000000000800}\r\nProcessId: 5992\r\nImage: C:\\WINDOWS\\Explorer.EXE\r\nTargetFilename: C:\\Users\\Sec User\\Downloads\\atomic-red-team-master\\atomic-red-team-master\\atomics\\T1614.001\\bin\\LanguageKeyboardLayout.exe\r\nCreationUtcTime: 2025-09-05 10:52:40.000\r\nPreviousCreationUtcTime: 2025-09-07 07:37:43.913\r\nUser: DESKTOP-K05T3EJ\\Sec User","EventData":["T1099","2025-09-07 07:37:43.913","{B2A55EDD-95D0-68B5-7A07-000000000800}","5992","C:\\WINDOWS\\Explorer.EXE","C:\\Users\\Sec User\\Downloads\\atomic-red-team-master\\atomic-red-team-master\\atomics\\T1614.001\\bin\\LanguageKeyboardLayout.exe","2025-09-05 10:52:40.000","2025-09-07 07:37:43.913","DESKTOP-K05T3EJ\\Sec User"]}
{"ProviderName":"Microsoft-Windows-Sysmon","ProviderGUID":"","EventID":"16","Level":"4","Task":"16","Opcode":"0","Keywords":"0x8000000000000000","TimeCreated":"2025/09/07 08:07:09.989897600","EventRecordID":"30201","ActivityID":"","RelatedActivityID":"","ProcessID":"10824","ThreadID":"1764","Channel":"Microsoft-Windows-Sysmon/Operational","Computer":"DESKTOP-K05T3EJ","UserID":"S-1-5-21-647405284-1499250508-452445211-1001","User":"DESKTOP-K05T3EJ\\Sec User","Version":"3","Description":"Sysmon config state changed:\r\nUtcTime: 2025-09-07 08:07:09.988\r\nConfiguration: C:\\Users\\Sec User\\Downloads\\Sysmon\\sysmonconfig-export.xml\r\nConfigurationFileHash: SHA256=055FEBC600E6D7448CDF3812307275912927A62B1F94D0D933B64B294BC87162","EventData":["2025-09-07 08:07:09.988","C:\\Users\\Sec User\\Downloads\\Sysmon\\sysmonconfig-export.xml","SHA256=055FEBC600E6D7448CDF3812307275912927A62B1F94D0D933B64B294BC87162"]}
```

Also add all the other pasers, so it will be parsed, before sending the events to indexing. 