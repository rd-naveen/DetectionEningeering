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