#/bin/bash

sudo touch /var/log/suricata/eve-alerts.json.pos
sudo chown core_user /var/log/suricata/eve-alerts.json.pos
sudo chmod o+w  /var/log/suricata/eve-alerts.json.pos

sudo touch /var/log/apache2/error.log.pos
sudo chown core_user /var/log/apache2/error.log.pos
sudo chmod o+w  /var/log/apache2/error.log.pos

sudo touch /var/log/apache2/access.log.pos
sudo chown core_user /var/log/apache2/access.log.pos
sudo chmod o+w  /var/log/apache2/access.log.pos

sudo touch /opt/zeek/logs/current/conn.log.pos
sudo chown core_user /opt/zeek/logs/current/conn.log.pos
sudo chmod o+w  /opt/zeek/logs/current/conn.log.pos

sudo touch /opt/zeek/logs/current/dns.log.pos
sudo chown core_user /opt/zeek/logs/current/dns.log.pos
sudo chmod o+w  /opt/zeek/logs/current/dns.log.pos

sudo touch /opt/zeek/logs/current/http.log.pos
sudo chown core_user /opt/zeek/logs/current/http.log.pos
sudo chmod o+w  /opt/zeek/logs/current/http.log.pos

sudo touch /opt/zeek/logs/current/ssl.log.pos
sudo chown core_user /opt/zeek/logs/current/ssl.log.pos
sudo chmod o+w  /opt/zeek/logs/current/ssl.log.pos

sudo touch /opt/zeek/logs/current/files.log.pos
sudo chown core_user /opt/zeek/logs/current/files.log.pos
sudo chmod o+w  /opt/zeek/logs/current/files.log.pos

sudo touch /opt/zeek/logs/current/known_hosts.log.pos
sudo chown core_user /opt/zeek/logs/current/known_hosts.log.pos
sudo chmod o+w  /opt/zeek/logs/current/known_hosts.log.pos

sudo touch /opt/zeek/logs/current/files.log.pos
sudo chown core_user /opt/zeek/logs/current/files.log.pos
sudo chmod o+w  /opt/zeek/logs/current/files.log.pos

sudo touch /opt/zeek/logs/current/known_services.log.pos
sudo chown core_user /opt/zeek/logs/current/known_services.log.pos
sudo chmod o+w  /opt/zeek/logs/current/known_services.log.pos

sudo touch /opt/zeek/logs/current/ntp.log.pos
sudo chown core_user /opt/zeek/logs/current/ntp.log.pos
sudo chmod o+w  /opt/zeek/logs/current/ntp.log.pos

sudo touch /opt/zeek/logs/current/software.log.pos
sudo chown core_user /opt/zeek/logs/current/software.log.pos
sudo chmod o+w  /opt/zeek/logs/current/software.log.pos

sudo touch /opt/zeek/logs/current/x509.log.pos
sudo chown core_user /opt/zeek/logs/current/x509.log.pos
sudo chmod o+w  /opt/zeek/logs/current/x509.log.pos

sudo touch /opt/zeek/logs/current/dhcp.log.pos
sudo chown core_user /opt/zeek/logs/current/dhcp.log.pos
sudo chmod o+w  /opt/zeek/logs/current/dhcp.log.pos

sudo touch /opt/zeek/logs/current/pe.log.pos
sudo chown core_user /opt/zeek/logs/current/pe.log.pos
sudo chmod o+w  /opt/zeek/logs/current/pe.log.pos

sudo touch /opt/zeek/logs/current/quic.log.pos
sudo chown core_user /opt/zeek/logs/current/quic.log.pos
sudo chmod o+w  /opt/zeek/logs/current/quic.log.pos

sudo touch /opt/zeek/logs/current/weird.log.pos
sudo chown core_user /opt/zeek/logs/current/weird.log.pos
sudo chmod o+w /opt/zeek/logs/current/weird.log.pos

