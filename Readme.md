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
| Windows | Operating System | Done
| Linux | Opearting System| -
| ModSecurity | Security| -
| Firewall |Security| -