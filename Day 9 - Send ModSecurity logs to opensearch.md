By default Modsecurity does not log in JSON format, to make it work we need to modify the `modsecurity.conf` file

`sudo nano /etc/modsecurity/modsecurity.conf`

and Add the below lines after  `SecAuditLogParts ABDEFHIJZ`

`SecAuditLogFormat JSON`

The output file is not usually readable by others, hence we need to change the perm
`sudo chmod o+r  /var/log/apache2/modsec_audit.log`

Add the below lines in the fluentd.conf file
```
<source>
     @type tail
     path /var/log/apache2/modsec_audit.log
     #pos_file /var/log/suricata/eve-alerts.json.pos
     <parse>
        @type json
     </parse>
     path_key  tailed_path
     tag events.security.modsecurity
     emit_unmatched_lines true
</source>

```


To test if the modsecurity is working correctly or not, try `curl "http://coreserver/?foo=/etc/passwd&bar=/bin/sh" -I`


Now we should be able to see the logs in the opensearch...