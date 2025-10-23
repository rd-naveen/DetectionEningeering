## List of things to try(related to Detection Engineering)
- [X]  Collect logs from windows and linux system.
    - [X] Linux
    - [X] Windows
- [X] Parse logs
   - [X] Use Regular Expressions
   - [X] Json Parsing 
- [ ] Enrich logs
- [X] Send Logs to OpenSearch
- [ ] Detection
    - [ ] Create Detector/Alert/Correlation Rules
    - [ ] Dashboards
    - [ ] Assets/User Dashboards
    - [ ] Top Stats
    - [ ] Security Tool specific Dashboards
        - [ ] Suricata
        - [ ] Zeek
        - [ ] ModSecurity 



- [ ] Automation/workflow framework - Airflow
    - [ ] Install and configure Airflow in ubuntu
    - [ ] Pull sample feeds
    - [ ] Pull reports from Opensearch
    - [ ] Get stats report from Fluentd


## Integrations Status 
| Log Name    | Type | Parsing | Enrichment | Indexing |Alerts | Correlation | Play book | Dashboard
| -------- | ------- |------- | ------- |------- |------- |------- |------- |------- |
| Zeek  | Network | Done
| Apache2 | Application |Done
| Suricata | Security | Done
| Windows-System | Operating System | Done
| Windows-Security | Operating System | Done
| Windows-Application | Operating System | Done
| Windows-Scheduling | Operating System | Done
| Linux-Auth | Opearting System| Done
| Linux-auditd | Opearting System| Done
| ModSecurity | Security| Done
| Sysmon |Security| Done 


## Lab Setup

### Network Traffic Flow
![alt text](.\images\traffic-flow.png)

### Events Flow
![alt text](.\images\events-flow.png)