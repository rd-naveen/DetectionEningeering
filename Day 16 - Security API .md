How to take backup of 
* Log Types
* Mappings
* Detectors
* Ruless
* Threat Intel Config

Note: Currently I'm think that we should have a local/git repository of the all the rules we have created in the Opensearch Security Analytics, and If we change anything in the local, it should relfect in the security analytics also. 


Important Indexes

.opensearch-sap-correlation-alerts
.opensearch-sap-correlation-metadata
.opensearch-sap-correlation-rules-config
.opensearch-sap-custom-rules-config
.opensearch-sap-detectors-config
.opensearch-sap-log-types-config
.opensearch-sap-sysmon-events-alerts
.opensearch-sap-sysmon-events-alerts-history
.opensearch-sap-sysmon-events-alerts-history-2025.09.09-1
.opensearch-sap-sysmon-events-detectors-queries-optimized-3ff11636-1c30-42e7-97fa-bc0b7a83b288
.opensearch-sap-sysmon-events-detectors-queries-optimized-3ff11636-1c30-42e7-97fa-bc0b7a83b288-000001
.opensearch-sap-sysmon-events-findings
.opensearch-sap-sysmon-events-findings-2025.09.09-1



Get log soruces/types
* To create a log type (we won't use this)
```
POST /_plugins/_security_analytics/logtype
{
  "description": "custom-log-type-desc",
  "name": "custom-log-type4",
  "source": "Custom"
}
```


* To check if given log type is already available or not (we need to use this before we create a rule with give log source)
```
POST /_plugins/_security_analytics/logtype/_search
{
  "query": {
    "match": {
      "name": "sysmon-events"
    }
  }
}
```

Get rule Data

* If we are trying to update the existing rule, we could retrive the rule data
```
#search known ruel id
POST /_plugins/_security_analytics/rules/_search?pre_packaged=false
{
  "query" :{
    "match": {
      "_id": "QgKpLpkBTBofSa-VNEFp"
    }
  }
}
```
* To get all the rules
```
POST /_plugins/_security_analytics/rules/_search?pre_packaged=false
{
  "query": {
    "match_all": {}
  }
}
```
Sample Results
```
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 7,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": ".opensearch-sap-custom-rules-config",
        "_id": "8B70ppgBne8WcmOvrwhH",
        "_version": 1,
        "_seq_no": 0,
        "_primary_term": 1,
        "_score": 1,
        "_source": {
          "category": "apache_access",
          "title": "Password file Accessed",
          "log_source": "apache_access",
          "description": "passwd keywrod in the http url field",
          "references": [],
          "tags": [
            {
              "value": "attack.webserver"
            }
          ],
          "level": "medium",
          "false_positives": [],
          "author": "Naveen",
          "status": "experimental",
          "last_update_time": "2025-08-14T00:00:00.000Z",
          "queries": [
            {
              "value": "url.original: *passwd*"
            }
          ],
          "query_field_names": [
            {
              "value": "url.original"
            }
          ],
          "aggregationQueries": [],
          "rule": """id: 25b9c01c-350d-4b95-bed1-836d04a4f324
title: Password file Accessed
description: passwd keywrod in the http url field
status: experimental
author: Naveen
date: 2025/08/14
modified: 2025/08/14
logsource:
  category: apache_access
level: medium
detection:
  condition: Selection_1
  Selection_1:
    url.original|contains:
      - passwd
tags:
  - attack.webserver
"""
        }
      },
    ]
  }
}
```
* To update a old rule

  TODO: As of now we are not able to perfom update/create rules, we are getting bellow error.

  ```
  {
  "error": {
    "root_cause": [
      {
        "type": "security_analytics_exception",
        "reason": "{\"error\":\"Sigma rule must have a log source\",\"error\":\"Sigma rule must have a detection definitions\"}"
      }
    ],
    "type": "security_analytics_exception",
    "reason": "{\"error\":\"Sigma rule must have a log source\",\"error\":\"Sigma rule must have a detection definitions\"}",
    "caused_by": {
      "type": "exception",
      "reason": "java.util.Arrays$ArrayList: {\"error\":\"Sigma rule must have a log source\",\"error\":\"Sigma rule must have a detection definitions\"}"
    }
  },
  "status": 400
}
  ```

Let try something differnt, I found that in the opensearch forum, a user posted that he used Curl to send yaml file (sigma) to the rule api. 

Why send sigma yaml file, do we have option to import yaml file in the UI. 
  yes, http://coreserver:5601/app/opensearch_security_analytics_dashboards#/import-rule

So all we need to send the data to this API.


I copied the HTTP request sent during the Above UI usage as a curl command, now it works. 
```
curl 'http://coreserver:5601/_plugins/_security_analytics/rules?dataSourceId=' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-US,en;q=0.9,en-IN;q=0.8' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -b 'security_authentication=Fe26.2**90d4b674c635470085474e991ef370a3fc6c3b41b188f25ea6a6cf7e15c3b542*3GaKU0LGfr3t9Wfl_BW63w*-KcJk4tZm0ziNZGd6-po3O2uk11VfWwN0vAJ9hTCnb-BYZQ721TJCsSMAwzEPYDwiiMSSbkRAqe_xGb9FM4BBxKG5ABi1qvtLeWBdLYUwAMhACHd6IkvlSgL4OptAc6Ff8f8GhYIVDtQHypNf8aAM1FjNq3yUwT-VgqBwj1VwdQ31kMx3ycm87WRGma0xT1EvhanwoaUiXflBLi44MrBhXtBtB4boHJfclHkN_t_EyJlj19ICusHILnd_afMv-u1U7GHxxWtJgzVbio4KF1aBg**6ce0b1bd4839dad0e88af85c4cf96817f9ce9eb094ea4820e3c8a7d8d1b0e617*voGSepAsREYZghsBKcUe4_9KkG0YMHJFlPfBDLoMf_k' \
  -H 'Origin: http://coreserver:5601' \
  -H 'Referer: http://coreserver:5601/app/opensearch_security_analytics_dashboards' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0' \
  -H 'osd-version: 2.19.2' \
  -H 'osd-xsrf: osd-fetch' \
  --data-raw $'{"id":"25b9c01c-350d-4b95-bed1-836d04a4f324","category":"windows","title":"Moriya Rootkit","description":"Detects the use of Moriya rootkit as described in the securelist\'s Operation TunnelSnake report","status":"experimental","author":"Bhabesh Raj","references":[{"value":"https://securelist.com/operation-tunnelsnake-and-moriya-rootkit/101831"}],"tags":[{"value":"attack.persistence"},{"value":"attack.privilege_escalation"},{"value":"attack.t1543.003"}],"log_source":{"product":"windows","service":"system"},"detection":"selection:\\n  Provider_Name: Service Control Manager\\n  EventID: 7045\\n  ServiceName: ZzNetSvc\\ncondition: selection\\n","level":"critical","false_positives":[{"value":"Unknown"}]}' \
  --insecure
```
Now the question is how we can get the "security_authentication" value programatically or how we can send the data securely

 curl -X  POST "http://coreserver:9200/fluentd.events.security.windows-2025.09.12/_search?pretty" -ku admin:<redacted> -H 'Content-Type: application/json' -d '
{
  "query": {
    "match_all": {}
  }
}' > out.json

```
This also works

Note: in the data-raw might contain some new lines, we need to remove before pasting in the curl

```
curl 'http://coreserver:5601/_plugins/_security_analytics/rules?dataSourceId=' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-US,en;q=0.9,en-IN;q=0.8' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -ku admin:<redacted> \
  -H 'Origin: http://coreserver:5601' \
  -H 'Referer: http://coreserver:5601/app/opensearch_security_analytics_dashboards' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0' \
  -H 'osd-version: 2.19.2' \
  -H 'osd-xsrf: osd-fetch' \
  --data-raw $'{"id":"25b9c01c-350d-4b95-bed1-836d04a4f324","category":"windows","title":"Moriya Rootkit","description":"Detects the use of Moriya rootkit as described in the securelist\'s Operation TunnelSnake report","status":"experimental","author":"BhabeshRaj","references":[{"value":"https://securelist.com/operation-tunnelsnake-and-moriya-rootkit/101831"}],"tags":[{"value":"attack.persistence"},{"value":"attack.privilege_escalation"},{"value":"attack.t1543.003"}],"log_source":{"product":"windows","service":"system"},"detection":"selection:\\n  Provider_Name: Service Control Manager\\n  EventID: 7045\\n  ServiceName: ZzNetSvc\\ncondition: selection\\n","level":"critical","false_positives":[{"value":"Unknown"}]}' \
  --insecure
```