**What is Fluentd**: 
    Fluentd is an open-source data collector for a unified logging layer. Fluentd allows you to unify data collection and consumption for better use and understanding of data.
    
* Fluentd treats logs as JSON, a popular machine-readable format. It is written primarily in C with a thin-Ruby wrapper that gives users flexibility.

    - ref: https://www.fluentd.org/images/fluentd-architecture.png

* Key features: 
        - Unified logging with JSON
        - Pluggable architecture (plugins) - data sources and data outputs 
        - Minimum resource requried (30-40MB) for 13k events/core/second, for less the 450k size memory constrains use fluentbit as lightweight forwarder
        - built-in reliablity - in-memory and file based buffering, failover and high-availability

    ref: https://www.fluentd.org/ and https://docs.fluentd.org/

* Life cycle of a Fluentd event: 
        - Setups, input, filter, matches, labels

        - configuration file, allows us to define which Inputs or listeners Fluentd will have and set up common matching rules to route the Event data to a specific Output. 

* Event structure: 
    - tag: Specifies the origin where an event comes from. It is used for message routing
    - time: Specifies the time when an event happens with nanosecond resolution
    - record: Specifies the actual log as a JSON object. 

            example:
            ```
            tag: apache.access         # set by configuration
            time: 1362020400.000000000 # 28/Feb/2013:12:00:00 +0900
            record: {"user":"-","method":"GET","code":200,"size":777,"host":"192.168.0.1","path":"/"}
            ```
* Configuration file examples: The definition specifies that an HTTP server will be listening on TCP port 8888

    ```
    <source>
        @type http
        port 8888
        bind 0.0.0.0
    </source>
    ```      

    ```
    <match test.cycle>
        @type stdout
    </match>
    ```
    The Match sets a rule where each Incoming event that arrives with a Tag equals to test.cycle, will match and use the Output plugin type called stdout


    A Filter behaves like a rule to pass or reject an event. The following configuration adds a Filter definition:

    ```
    <filter test.cycle>
        @type grep
        <exclude>
            key action
            pattern ^logout$
        </exclude>
    </filter>
    ```
    The Filter basically will accept or reject the Event based on its type and rule. For our example we want to discard any user logout action. We only care about the logins. The way to accomplish this, is doing a grep inside the Filter to exclude any message on which action key have the logout string.


    This new implementation called Labels, aims to solve the configuration file complexity and allows to define new Routing sections that do not follow the top-to-bottom order, instead they act like linked references. Taking the previous example, we will modify the setup as follows

    ```
    <source>
        @type http
        bind 0.0.0.0
        port 8888
        @label @STAGING
    </source>

    <filter test.cycle>
        @type grep
        <exclude>
            key action
            pattern ^login$
        </exclude>
    </filter>

    <label @STAGING>
        <filter test.cycle>
            @type grep
            <exclude>
            key action
            pattern ^logout$
            </exclude>
        </filter>

        <match test.cycle>
            @type stdout
        </match>
    </label>
    ```
    The source definition contains a @lable parameter under source, indicating that the flow should continue inside the @STAGING label section. 
            
    Also, this flow redirect happens for every event reported on the Source, the Routing Engine will continue processing on @STAGING. Hence, it will skip the old filter definition.


**Installing Fluentd in ubuntu**: 
        1- Increase the maximum number of file descriptors. 
        $ ulimit -n # to view the numerbr of file descriptors allowed
        if above command returns 1024, then change the file /etc/security/limits.conf file and reboot your machine
        
        $ sudo nano /etc/security/limits.conf
            ```
            root soft nofile 65536
            root hard nofile 65536
            * soft nofile 65536
            * hard nofile 65536
            ```

        $ sudo init 6

        2- install fluentd package in debian. 

        Use below command to find which ubuntu version/codename you are running, 
        $ cat /etc/os-release

        and execute the below curl command to download and run the script. 
        TIP: try to install the LTS version of the package

        $ sudo curl -fsSL https://toolbelt.treasuredata.com/sh/install-ubuntu-noble-fluent-package5-lts.sh | sh

        once installed it should automatically start the service. 

        $ sudo systemctl status fluentd.service
        $ sudo systemctl start fluentd.service

        3- test the fluentd setup

        The default configuration (/etc/fluent/fluentd.conf) is to receive logs at an HTTP endpoint and route them to stdout
        $ curl -X POST -d 'json={"json":"message"}' http://localhost:8888/debug.test

        $ tail -n 1 /var/log/fluent/fluentd.log
        2018-01-01 17:51:47 -0700 debug.test: {"json":"message"}


    TODO: 
        Read apache logs and Print them in the stdout (json, will later send it to the opensearch or anywhere)

        add below lines inthe /var/log/fluent/fluentd.log file
        ```
        <source>
            @type tail
            path "/var/log/apache2/access.log"
            pos_file "/var/log/fluent/apache2.access_log.pos"
            tag "core_server_apache2"
            <parse>
                @type "apache2"
            </parse>
        </source>
        <match core_server_*>
            @type stdout
        </match>
        
        ```

        create this file /var/log/fluent/apache2.access_log.pos using touch and make sure the user _fluentd can write this file, or make this file writable by other
        
        chmod o+w /var/log/fluent/apache2.access_log.pos # though not secure

        TODO: how we can make sure that fluent can write the above file, without making others able to write this file. 

        To test if the configuration works: 

        $fluentd -c /etc/fluent/fluentd.conf

        and execute below curl command in another terminal or open the web page in webbrowser. 
        $ curl http://localhost

        After executing the curl command, In the fluentd command windows, we should be able to see new entry with similar to below resutls. 

        2025-08-26 12:33:19.000000000 +0000 core_server_apache2: {"host":"::1","user":null,"method":"GET","path":"/","code":200,"size":10926,"referer":null,"agent":"curl/8.5.0"}

        or 

        2025-08-26 12:36:10.000000000 +0000 core_server_apache2: {"host":"172.18.0.1","user":null,"method":"GET","path":"/","code":200,"size":3460,"referer":null,"agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"}

**Installing Fluentd in windows**:
* install the msi package from the official fluentd site {note the installation directory}
* edit the fluentd.conf file inside the installation directory c:\opt\fluent\etc\fluent\fluentd.conf
                add source and match definitions

    ```
    <source>
        @type windows_eventlog2
        @id windows_eventlog2
        channels security
        read_existing_events false
        tag winevt.raw
        rate_limit 200
        <storage>
            @type local
            persistent true
            path C:\opt\fluent\winlog.json
        </storage>
    </source>

    <match winevt.raw>
        @type stdout
    </match>            
    ```

    or forward the event to another fluentd device. 

        ** on device which sends the data.
        <source>
            @type windows_eventlog2
            channels ["security","system","application","Microsoft-Windows-Sysmon/Operational"]
            read_existing_events false
            tag winevt.raw
            # rate_limit 200
            <storage>
                @type local
                persistent true
                path C:\opt\fluent\winlog.json
            </storage>
        </source>

        <match winevt.*>
            @type forward
            send_timeout 60s
            recover_wait 10s
            hard_timeout 60s
            <server>
                name coreserver
                host 10.10.10.100
                port 24224
                weight 60
            </server>
        </match>

        ** on device which receives the data.
        ```
        <source>
            @type forward
            port 24224
            bind "0.0.0.0"
            tag "events.security.windows"
        </source>
        ```

    NOTE: When used hostname instead of IP(IPv4), we are not able to recive the logs in the receiver fluentd, possibly because IPv6 is used.


    Note: when forwarding the logs to remote fluentd device, the tag is  "winevt.raw", but during the receving end, we modified it to "events.security.windows". We could also use the tag from the source fluentd to make new tag.
    
    ```
    // when used hostname
    2025-08-26 18:32:15 +0530 [warn]: #0 detached forwarding server 'coreserver' host="coreserver" port=24224 phi=16.010400375908784 phi_threshold=16
    ```

    ```
    // when used ipv6
    2025-09-01 06:38:25 -0700 [warn]: #0 detached forwarding server 'coreserver' host="fe80::215:5dff:fe01:2205" port=24224 phi=16.02555785288765 phi_threshold=16
    ```