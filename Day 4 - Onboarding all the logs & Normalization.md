## Importaance of Normalization
* Common fields across all te log sources, it will make easier for querying and correlation.
    Most important field we need to correlate.
    *   Source and Destination ports and IP address
    *   User Names, Host/Device Names
    *   Alert/Event Messages

    Refer: https://ossemproject.com/cdm/intro.html for more standard way to normalize the event sources. 

Before we start normalizing events, Let's make sure we have below log sources configured correctly. 

    Aapche2 - Done
    Suricata - Done
    Zeek/Bro - Done
    Windows Security Events
    Windows Sysmon
    Linux Auth
        /var/log/faillog
        /var/log/auth.log
        /var/log/apt/term.log or /var/log/dpkg.log

### Input Sources
```
<source>
        @type tail
        path /opt/zeek/logs/current/*.log
        exclude_path ["/opt/zeek/logs/current/stats.log","/opt/zeek/logs/current/telemetry.log","/opt/zeek/logs/current/stdout.log","/opt/zeek/logs/current/stderr.log","/opt/zeek/logs/current/capture_loss.log","/opt/zeek/logs/current/reporter.log"]
        pos_file /opt/zeek/logs/current/zeek.pos
        path_key tailed_path
        refresh_interval 5
        <parse>
                @type json
        </parse>
        tag core_server_zeek
</source>
<source>
        @type tail
        path /var/log/suricata/eve-alerts.json
        pos_file /var/log/suricata/eve.json.pos
        <parse>
        @type json
        </parse>
        tag core_server_suricata
</source>

<source>
        @type tail
        path /var/log/apache2/access.log
        pos_file /var/log/fluent/apache2.access_log.pos
        <parse>
                @type apache2
        </parse>
        tag core_server_apache2
</source>
```

### Filters
```
<filter core_server_zeek>
        @type record_transformer
        <record>
                "source.ip" ${record["id.orig_h"]}
                "source.port" ${record["id.orig_p"]}
                "destination.ip" ${record["id.resp_h"]}
                "destination.port" ${record["id.resp_p"]}
                "zeek.connection.id" ${record["uid"]}
                "hostname" ${record["query"]}
                #"hostname" ${record["server_name"]}
        </record>
        remove_keys id.orig_h,id.orig_p,id.resp_h,id.resp_p
</filter>

<filter core_server_apache2>
        @type record_transformer
        <record>
                "hostname" ${record["host"]}
                "source.ip" ${record["host"]}
                "log.source" ${tag}
                "request.method" ${record["method"]}
                "request.uri" ${record["path"]}
                "request.response_code" ${record["code"]}
                "response.size" ${record["size"]}
                "request.referer" ${record["referer"]}
                "request.user_agent" ${record["agent"]}
        </record>
        remove_keys host,method,path,code,size,referer,agent
</filter>

<match core_server_zeek*>
  @type stdout
</match>
```


### Known Issues:
For some logs, if the transforming fiels is not available in the logs, it's throwing error and also adding null values to that field. It might generate noise. Hence we need to find a alternate way to safely add this. or create a transformer for each of the records. 