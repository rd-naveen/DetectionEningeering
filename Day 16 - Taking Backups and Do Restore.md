How to take backup of 
* Log Types
* Mappings
* Detectors
* Ruless
* Threat Intel Config

Note: Currently I'm think that we should have a local/git repository of the all the rules we have created in the Opensearch Security Analytics, and If we change anything in the local, it should relfect in the security analytics also. 

    Then what about exitin alert histories, and rules where they are stored. 




A. Taking Backup of Log Types and Do Restoration

```
POST /_plugins/_security_analytics/logtype/_search
{
    "query": {
        "match_all": {}
    }
}
```

```
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 26,
      "relation": "eq"
    },
    "max_score": 2,
    "hits": [
      {
        "_index": ".opensearch-sap-log-types-config",
        "_id": "7J0TQ5kB0sFaUg96xucq",
        "_score": 2,
        "_source": {
          "name": "test-log-type",
          "description": "Test Log Type",
          "category": "Other",
          "source": "Custom",
          "tags": {
            "correlation_id": 28
          }
        }
      },
      //..... other log types goes here
    ]
  }
}
```

let take below log type `test-log-type` check how we can take a backup and do restore.

``
{
    "_index": ".opensearch-sap-log-types-config",
    "_id": "7J0TQ5kB0sFaUg96xucq",
    "_score": 2,
    "_source": {
        "name": "test-log-type",
        "description": "Test Log Type",
        "category": "Other",
        "source": "Custom",
        "tags": {
        "correlation_id": 28
        }
    }
}
``

To Create a Log type: 

```
POST /_plugins/_security_analytics/logtype
{
  "description": "custom-log-type-desc",
  "name": "custom-log-type4",
  "source": "Custom"
}
```

To Update A log Type:
```
//To get the log type id
POST /_plugins/_security_analytics/logtype/_search
{
    "query": {
        "match_phrase_prefix": {
          "name": "custom-log-type5"
        }
    }
}

//"_id": "DJ05Q5kB0sFaUg96vOrJ"
PUT /_plugins/_security_analytics/logtype/DJ05Q5kB0sFaUg96vOrJ
{
  "name": "custom-log-type5",
  "description": "custom-log-type-updated-desc",
  "source": "Custom"
}
```

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





Get detector Types