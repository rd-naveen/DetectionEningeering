***Fluentd Parsing***

Fluentd provides parsing options for some common log type. But for other logs we probably need to manually 

ref: https://docs.fluentd.org/parser

List of builtin parsers: 
* *regexp*
* *apache2*
* apache_error
* ngnix
* syslog
* csv
* tsv
* ltsv
* *json*
* msgpack
* multiline
* none

3rd Party parsers: 
* Grok
* Avro


**Example: Regexp**

let's try to parse the suricata IDS logs, using `regexp`

sample records if we execute `watch -n 3 "curl http://testmynids.org/uid/index.html"`
*Above command will trigger default suricata rules, and it will execute the curl command on every 3 seconds. So it will be easy for the testing.

`
08/27/2025-09:34:55.480642  [**] [1:2100498:7] GPL ATTACK_RESPONSE id check returned root [**] [Classification: Potentially Bad Traffic] [Priority: 2] {TCP} 18.161.246.41:80 -> 10.10.10.100:58564
`
```
<source>
        @type tail
        path /var/log/suricata/fast.log
        pos_file /var/log/suricata/fast.log.pos
        <parse>
                @type regexp
                expression /^(?<eventtime>[\d\/\-\:\.]*)\s+\[\*\*\] \[\d+\:(?<suricata_sig_id>\d+)\:(?<suricata_sig_rev_id>\d+)\] (?<suricata_message>[^\[]+) \[\*\*\] \[Classification\: (?<suricata_classification>[^\]]*)\] \[Priority\: (?<suricata_priority>\d+)\] \{(?<suricata_protocol>\w+)\} (?<source_ip>[^\:]*)\:(?<source_port>[^ ]*) \-\> (?<destination_ip>[^\:]*)\:(?<destination_port>[^ ]*).*/
                time_key event_time
                types suricata_sig_id:integer
                types suricata_sig_rev_id:integer
        </parse>
        tag core_server_suricata
</source>
```

To match spaces (more than one space's use \s+, instead of the plain `  `, we can use the https://fluentular.herokuapp.com/ or https://regex101.com/ to verify the regular expressions)

```
<match core_server_*>
  @type stdout
</match>
```

after saving the changes restart the fluentd with our custom configuration. `fluentd -c /etc/fluent/fluentd.conf`

The stdout terminal should give use the below results. 
`
2025-08-27 09:34:55.489486737 +0000 core_server_suricata: {"eventtime":"08/27/2025-09:34:55.480642","suricata_sig_id":"2100498","suricata_sig_rev_id":7,"suricata_message":"GPL ATTACK_RESPONSE id check returned root","suricata_classification":"Potentially Bad Traffic","suricata_priority":"2","suricata_protocol":"TCP","source_ip":"18.161.246.41","source_port":"80","destination_ip":"10.10.10.100","destination_port":"58564"}
`

If we get " #0 pattern not matched: " error try to remove the patterns and change the pattern incrementaly to test each of the regex element is working or not.


**Example: json**

Suricata IDS also supports by default json formated outputs, if it is not enabled or currently disabled we can re-enable them by modifying the configuration file. 

In the file `/etc/suricata/suricata.yaml` locate below lines and change the `eve-log` to `enabled: yes`

and restart the suricata service using `sudo service suricata restart` and verify the same using `sudo service suricata status`

If we execute the `watch -n 3 "curl http://testmynids.org/uid/index.html"` now, we should be able to see some new entries in the `/var/log/suricata/eve.json`. 

`{"timestamp":"2025-08-27T09:50:46.970827+0000","flow_id":1801364899640642,"in_iface":"eth0","event_type":"fileinfo","src_ip":"18.161.246.76","src_port":80,"dest_ip":"10.10.10.100","dest_port":38580,"proto":"TCP","ip_v":4,"pkt_src":"wire/pcap","community_id":"1:ddEEV+m9yfLHr2UtkHv3R0t9lAI=","http":{"hostname":"testmynids.org","url":"/uid/index.html","http_user_agent":"curl/8.5.0","http_content_type":"text/html","http_method":"GET","protocol":"HTTP/1.1","status":200,"length":39},"app_proto":"http","fileinfo":{"filename":"/uid/index.html","gaps":false,"state":"CLOSED","stored":false,"size":39,"tx_id":0}}`

Now let's try to parse these entries using `json` parser

```
<source>
        @type tail
        path /var/log/suricata/eve.json
        pos_file /var/log/suricata/eve.json.pos
        <parse>
            @type json
        </parse>
        tag core_server_suricata
</source>
```
and we should be able to see the same records in the `eve.json` to the stdout terminal.


So far we have read and parse the data from apache2, suricata logs and we also know how to read new/custom logs using regex. Now let's try to parse the zeek logs. 


**Example: Zeek logs parsing**

To make sure the zeek produces the logs in json format, we need to enable it . 

Go to the zeek installation directory, in my case `/opt/zeek/` and modify the file `/opt/zeek/share/zeek/site` by adding new entry on the top of the file `@load policy/tuning/json-logs.zeek`

Deloy these configurations `sudo ./zeekctl deploy` and make sure there is no error in the zeek services `sudo ./zeekctl status`. 

And verify if we are able to see the logs in json format or not. `/opt/zeek/logs/current$ tail -f http.log`

Now let's try to parse these files using fluentd and json parser.Since we have many files, for now will read only few files. 
```
<source>
        @type tail
        path /opt/zeek/logs/current/http.log
        pos_file /opt/zeek/logs/current/http.log.pos
        <parse>
                @type json
        </parse>
        tag core_server_zeek_http
</source>
```
Now we should be able to see the results, in the stdout as json format. 

`2025-08-27 10:34:31.562901366 +0000 core_server_zeek_http: {"ts":1756290871.13984,"uid":"Cx1A6RUp88rZZZvH3","id.orig_h":"10.10.10.100","id.orig_p":57186,"id.resp_h":"18.161.246.67","id.resp_p":80,"trans_depth":1,"version":"1.1","request_body_len":0,"response_body_len":39,"status_code":200,"status_msg":"OK","tags":[],"resp_fuids":["F77xkx2S7xA5Ce46uk"],"resp_mime_types":["text/plain"]}
`

Strange Part is even though we are reading from the http log, we are not seeing the http request fields, such as hostname, uri, etc. Need to ceck this in the next experiment. 


## Field Mapping issue:

In the opensearch-dashboard, when trying to filter the field, It'll show Mapping is not available to this field. In this we need to re-map them, let's see how we can do that. 

Why this issue is happening? As we dynmaically integrate more and more log sources, each logs might have different fields, but we haven't refershed mapping. this causes issue when we try to filter something which is not mapped.  

1. Goto Dashboard management -> Index Patterns -> Delete the pattern associated with fluentd.events.*
    ![alt text](images/image-3.png)

2. Create a new index pattern by selecting all the relevant indexes, and make sure now all the field types are selected correctly.

    ![alt text](images/image-4.png)
    ![alt text](images/image-5.png)
    ![alt text](images/image-6.png)

3. Goto Index Management -> Indexes -> Select all the indexes we need to work on. 
    select all the relevant indexes, Action -> Clear Cache. 

    ![alt text](images/image-2.png)

4. Now if we reload the patterns and refresh the logs, we should be able to use the field for analytics.

See you in the next exploration !!!


Issue 1: Not all data from the sysmon is mapped to the file, instead they are present in the `Description` or `EventData`
    After fixing the Issue 2, We need to do the re-mapping of fields, in the opensearch-dashboard.

![alt text](images/sysmon_issue.png)

Issue 2: we have multiple sysmon events, we need to carefully extract them, as `Description` for each sysmon event id is differnce, hence we need to create a regex differently.
    For this we can create a small python script to generate new patterns based on given log. 

Example if the log for process creation event is as below

```
    log_= """Process Create:\r\nRuleName: -\r\nUtcTime: 2025-09-06 15:19:52.355\r\nProcessGuid: {b2a55edd-5118-68bc-bd17-000000000800}\r\nProcessId: 2112\r\nImage: C:\\Windows\\System32\\ctfmon.exe\r\nFileVersion: 10.0.26100.3624 (WinBuild.160101.0800)\r\nDescription: CTF Loader\r\nProduct: Microsoft® Windows® Operating System\r\nCompany: Microsoft Corporation\r\nOriginalFileName: CTFMON.EXE\r\nCommandLine: /QuitInfo:0000000000000250;000000000000024C; \r\nCurrentDirectory: C:\\WINDOWS\\system32\\\r\nUser: DESKTOP-K05T3EJ\\Sec User\r\nLogonGuid: {b2a55edd-95cf-68b5-7004-cd0000000000}\r\nLogonId: 0xCD0470\r\nTerminalSessionId: 2\r\nIntegrityLevel: High\r\nHashes: MD5=A3E50EF69038B3415A4D75820255A301,SHA256=F219F0975E70935D0BD4898BC568B146603C1D2E07ECE027F5E5B5E4EAD203D5,IMPHASH=B539389D4BE1DD68C8213A539FEB41FB\r\nParentProcessGuid: {b2a55edd-a48c-68b1-3d00-000000000800}\r\nParentProcessId: 2844\r\nParentImage: C:\\Windows\\System32\\svchost.exe\r\nParentCommandLine: C:\\WINDOWS\\System32\\svchost.exe -k LocalSystemNetworkRestricted -p -s TextInputManagementService\r\nParentUser: NT AUTHORITY\\SYSTEM"""
```

And, Generated pattern using our small script is

```
Process Create:(?:\r?\n)(?:RuleName:\s+(?<RuleName>[^\r\n]+))(?:\r?\n)(?:UtcTime:\s+(?<UtcTime>[^\r\n]+))(?:\r?\n)(?:ProcessGuid:\s+(?<ProcessGuid>[^\r\n]+))(?:\r?\n)(?:ProcessId:\s+(?<ProcessId>[^\r\n]+))(?:\r?\n)(?:Image:\s+(?<Image>[^\r\n]+))(?:\r?\n)(?:FileVersion:\s+(?<FileVersion>[^\r\n]+))(?:\r?\n)(?:Description:\s+(?<Description>[^\r\n]+))(?:\r?\n)(?:Product:\s+(?<Product>[^\r\n]+))(?:\r?\n)(?:Company:\s+(?<Company>[^\r\n]+))(?:\r?\n)(?:OriginalFileName:\s+(?<OriginalFileName>[^\r\n]+))(?:\r?\n)(?:CommandLine:\s+(?<CommandLine>[^\r\n]+))(?:\r?\n)(?:CurrentDirectory:\s+(?<CurrentDirectory>[^\r\n]+))(?:\r?\n)(?:User:\s+(?<User>[^\r\n]+))(?:\r?\n)(?:LogonGuid:\s+(?<LogonGuid>[^\r\n]+))(?:\r?\n)(?:LogonId:\s+(?<LogonId>[^\r\n]+))(?:\r?\n)(?:TerminalSessionId:\s+(?<TerminalSessionId>[^\r\n]+))(?:\r?\n)(?:IntegrityLevel:\s+(?<IntegrityLevel>[^\r\n]+))(?:\r?\n)(?:Hashes:\s+(?<Hashes>[^\r\n]+))(?:\r?\n)(?:ParentProcessGuid:\s+(?<ParentProcessGuid>[^\r\n]+))(?:\r?\n)(?:ParentProcessId:\s+(?<ParentProcessId>[^\r\n]+))(?:\r?\n)(?:ParentImage:\s+(?<ParentImage>[^\r\n]+))(?:\r?\n)(?:ParentCommandLine:\s+(?<ParentCommandLine>[^\r\n]+))(?:\r?\n)(?:ParentUser:\s+(?<ParentUser>[^\r\n]+))
```

Then we can add the pattern in the fluentd.conf as below

You can also try the above pattern in the https://fluentular.herokuapp.com/ to check if the fields are correctly mapping are not.


```
<filter winevt.raw>
  @type parser
  key_name Description
  reserve_data true
  <parse>
    @type regexp
	expression /Process Create:(?:\r?\n)(?:RuleName:\s+(?<RuleName>[^\r\n]+))(?:\r?\n)(?:UtcTime:\s+(?<UtcTime>[^\r\n]+))(?:\r?\n)(?:ProcessGuid:\s+(?<ProcessGuid>[^\r\n]+))(?:\r?\n)(?:ProcessId:\s+(?<ProcessId>[^\r\n]+))(?:\r?\n)(?:Image:\s+(?<Image>[^\r\n]+))(?:\r?\n)(?:FileVersion:\s+(?<FileVersion>[^\r\n]+))(?:\r?\n)(?:Description:\s+(?<Description>[^\r\n]+))(?:\r?\n)(?:Product:\s+(?<Product>[^\r\n]+))(?:\r?\n)(?:Company:\s+(?<Company>[^\r\n]+))(?:\r?\n)(?:OriginalFileName:\s+(?<OriginalFileName>[^\r\n]+))(?:\r?\n)(?:CommandLine:\s+(?<CommandLine>[^\r\n]+))(?:\r?\n)(?:CurrentDirectory:\s+(?<CurrentDirectory>[^\r\n]+))(?:\r?\n)(?:User:\s+(?<User>[^\r\n]+))(?:\r?\n)(?:LogonGuid:\s+(?<LogonGuid>[^\r\n]+))(?:\r?\n)(?:LogonId:\s+(?<LogonId>[^\r\n]+))(?:\r?\n)(?:TerminalSessionId:\s+(?<TerminalSessionId>[^\r\n]+))(?:\r?\n)(?:IntegrityLevel:\s+(?<IntegrityLevel>[^\r\n]+))(?:\r?\n)(?:Hashes:\s+(?<Hashes>[^\r\n]+))(?:\r?\n)(?:ParentProcessGuid:\s+(?<ParentProcessGuid>[^\r\n]+))(?:\r?\n)(?:ParentProcessId:\s+(?<ParentProcessId>[^\r\n]+))(?:\r?\n)(?:ParentImage:\s+(?<ParentImage>[^\r\n]+))(?:\r?\n)(?:ParentCommandLine:\s+(?<ParentCommandLine>[^\r\n]+))(?:\r?\n)(?:ParentUser:\s+(?<ParentUser>[^\r\n]+))/
  </parse>
</filter>
```

The beauty of the above fluentd configuration is the if the logs matches the above regex, they will add the extracted fields, if not they won't add any field, and keep the original data, as we have added `reserve_data true`


For example, below is not relvant to the above pattern, hence the we don't add any new fields. 

```
2025-09-06 10:00:59.400054300 -0700 winevt.raw: {"ProviderName":"Microsoft-Windows-Sysmon","ProviderGUID":"","EventID":"8","Level":"4","Task":"8","Opcode":"0","Keywords":"0x8000000000000000","TimeCreated":"2025/09/06 17:00:56.953414400","EventRecordID":"19903","ActivityID":"","RelatedActivityID":"","ProcessID":"3544","ThreadID":"4200","Channel":"Microsoft-Windows-Sysmon/Operational","Computer":"DESKTOP-K05T3EJ","UserID":"S-1-5-18","User":"NT AUTHORITY\\SYSTEM","Version":"2","Description":"CreateRemoteThread detected:\r\nRuleName: -\r\nUtcTime: 2025-09-06 17:00:56.929\r\nSourceProcessGuid: {b2a55edd-95cb-68b5-6107-000000000800}\r\nSourceProcessId: 5156\r\nSourceImage: C:\\Windows\\System32\\dwm.exe\r\nTargetProcessGuid: {b2a55edd-95cb-68b5-5e07-000000000800}\r\nTargetProcessId: 2132\r\nTargetImage: C:\\Windows\\System32\\csrss.exe\r\nNewThreadId: 3848\r\nStartAddress: 0xFFFFF80059D97EC0\r\nStartModule: -\r\nStartFunction: -\r\nSourceUser: Window Manager\\DWM-2\r\nTargetUser: NT AUTHORITY\\SYSTEM","EventData":["-","2025-09-06 17:00:56.929","{B2A55EDD-95CB-68B5-6107-000000000800}","5156","C:\\Windows\\System32\\dwm.exe","{B2A55EDD-95CB-68B5-5E07-000000000800}","2132","C:\\Windows\\System32\\csrss.exe","3848","0xFFFFF80059D97EC0","-","-","Window Manager\\DWM-2","NT AUTHORITY\\SYSTEM"]}
```

But for the below, we are added few extraced fields. 

```
2025-09-06 10:02:13.390862300 -0700 winevt.raw: {"ProviderName":"Microsoft-Windows-Sysmon","ProviderGUID":"","EventID":"1","Level":"4","Task":"1","Opcode":"0","Keywords":"0x8000000000000000","TimeCreated":"2025/09/06 17:07:21.524316500","EventRecordID":"19921","ActivityID":"","RelatedActivityID":"","ProcessID":"3544","ThreadID":"4200","Channel":"Microsoft-Windows-Sysmon/Operational","Computer":"DESKTOP-K05T3EJ","UserID":"S-1-5-18","User":"DESKTOP-K05T3EJ\\Sec User","Version":"5","Description":"Ruby interpreter (CUI) 3.2.6p234 [x64-mingw-ucrt]","EventData":["-","2025-09-06 17:07:21.522","{B2A55EDD-6A49-68BC-AC18-000000000800}","3676","C:\\opt\\fluent\\bin\\ruby.exe","3.2.6p234","Ruby interpreter (CUI) 3.2.6p234 [x64-mingw-ucrt]","Ruby interpreter 3.2.6p234 [x64-mingw-ucrt]","http://www.ruby-lang.org/","ruby.exe","C:\\opt\\fluent\\bin\\ruby.exe -Eascii-8bit:ascii-8bit C:/opt/fluent/bin/fluentd -c C:\\opt\\fluent\\etc\\fluent\\fluentd.conf --under-supervisor","C:\\Users\\Sec User\\","DESKTOP-K05T3EJ\\Sec User","{B2A55EDD-95CF-68B5-3004-CD0000000000}","0x0000000000cd0430","2","High","MD5=E5608A47C9ECD83E8BCFC107EA6389B4,SHA256=8F095D6C8039CC3242A39BE1080665824198BF68DA05F923CDAD97004FF86396,IMPHASH=01DC7955A53767B850E59DE33ECA0850","{B2A55EDD-6A47-68BC-AA18-000000000800}","1944","C:\\opt\\fluent\\bin\\ruby.exe","\"C:\\opt\\fluent\\bin\\ruby.exe\"  \"C:\\opt\\fluent\\bin\\fluentd\" -c C:\\opt\\fluent\\etc\\fluent\\fluentd.conf","DESKTOP-K05T3EJ\\Sec User"],"RuleName":"-","UtcTime":"2025-09-06 17:07:21.522","ProcessGuid":"{b2a55edd-6a49-68bc-ac18-000000000800}","ProcessId":"3676","Image":"C:\\opt\\fluent\\bin\\ruby.exe","FileVersion":"3.2.6p234","Product":"Ruby interpreter 3.2.6p234 [x64-mingw-ucrt]","Company":"http://www.ruby-lang.org/","OriginalFileName":"ruby.exe","CommandLine":"C:\\opt\\fluent\\bin\\ruby.exe -Eascii-8bit:ascii-8bit C:/opt/fluent/bin/fluentd -c C:\\opt\\fluent\\etc\\fluent\\fluentd.conf --under-supervisor","CurrentDirectory":"C:\\Users\\Sec User\\","LogonGuid":"{b2a55edd-95cf-68b5-3004-cd0000000000}","LogonId":"0xCD0430","TerminalSessionId":"2","IntegrityLevel":"High","Hashes":"MD5=E5608A47C9ECD83E8BCFC107EA6389B4,SHA256=8F095D6C8039CC3242A39BE1080665824198BF68DA05F923CDAD97004FF86396,IMPHASH=01DC7955A53767B850E59DE33ECA0850","ParentProcessGuid":"{b2a55edd-6a47-68bc-aa18-000000000800}","ParentProcessId":"1944","ParentImage":"C:\\opt\\fluent\\bin\\ruby.exe","ParentCommandLine":"\"C:\\opt\\fluent\\bin\\ruby.exe\"  \"C:\\opt\\fluent\\bin\\fluentd\" -c C:\\opt\\fluent\\etc\\fluent\\fluentd.conf","ParentUser":"DESKTOP-K05T3EJ\\Sec User"}
```

As you can see some new fields are added, such as ParentUser, CommandLine, etc.

Similarly we need to added multiple patterns to capture other fields present in the sysmon events. without loosing 

TODO: Add patterns for each of the sysmon event types using examples. Can you do it everything at a same time, collect all log type formats, create pattern, and create fluentd config defnitions.