Linux logs onboarding

* Linux Auth
```
<source>
  @type tail
  path /var/log/auth.log
  pos_file /var/log/auth.pos
  <parse>
        @type none
        message_key auth_log
  </parse>
  tag events.security.linux.auth
</source>
// need to parse the log manually using regexp
```

* Linux dpkg
```
<source>
  @type tail
  path /var/log/dpkg.log
  pos_file /var/log/dpkg.pos
  <parse>
        @type none
        message_key dpkg_log
  </parse>
  tag events.security.linux.dpkg
</source>
// need to parse the logs manually
```

Note: when matching tags, if the tag has more than three component, then we also need to match them in the match section. 

```
<match events.security.linux.*>
@type stdout
</match>
```
or
```
<match events.security.*.*>
@type stdout
</match>
```

Note: If we use events.security.*, won't match the events.secrity.linux.dpkg logs

```
2025-09-01 14:23:53 +0000 [warn]: #0 no patterns matched tag="events.security.linux.dpkg"
```

Note: if we have two match patterns with the same pattern, only one is execute, need to check why and how to do it properly.

