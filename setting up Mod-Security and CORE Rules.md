Let's first install mod-security in the ubuntu server, where apache2 is already installed and running on port 80

Installation

`sudo apt install libapache2-mod-security2 -y`

`sudo a2enmod headers`

`sudo systemctl restart apache2`


Configuration

`sudo cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf`

`sudo nano /etc/modsecurity/modsecurity.conf` and change the value from `SecRuleEngine DetectionOnly` -> `SecRuleEngine On`

We probably, also need to change these values. Also the detections are tracked here `/var/log/apache2/modsec_audit.log`
```
SecAuditLogType Serial
SecAuditLog /var/log/apache2/modsec_audit.log
```

Configuring OWASP core rule set:

Note: Azure WAF also uses same/some of rules the core rule 
set from OWASP.

Delete the current ruleset if we have any
`sudo rm -rf /usr/share/modsecurity-crs`

Clone latest csr from git
`sudo git clone https://github.com/coreruleset/coreruleset /usr/share/modsecurity-crs`

Create a new configuration file from the template, provided with git repo
`sudo mv /usr/share/modsecurity-crs/crs-setup.conf.example /usr/share/modsecurity-crs/crs-setup.conf`


Enabling ModSecurity in Apache2 (`available` config files only)

add the below lines in the `sudo nano /etc/apache2/mods-available/security2.conf`
```
        IncludeOptional /etc/modsecurity/*.conf
        IncludeOptional /usr/share/modsecurity-crs/crs-setup.conf
        IncludeOptional /usr/share/modsecurity-crs/rules/*.conf
```

Open the Apache2 sites available configuration file, and add `SecRuleEngine On` in the config file, if we don't have any custom site files, default site file is available `/etc/apache2/sites-available`

Test the configuration using ` sudo apachectl configtest`

Now restart the Apache2 service using `sudo systemctl restart apache2` and verify the service using `sudo systemctl status apache2`

Testing the ModSecurity rules: 

We could use the `nikto` or any other opensource tools to scan the website and we should get the 403 responses, and the same should be logged in the  


curl "http://coreserver/?foo=/etc/passwd&bar=/bin/sh" -I

At the same time, we should see the logs in the `sudo tail -f /var/log/apache2/modsec_audit.log`


In next activity, we'll try to feed this data into Opensearch..