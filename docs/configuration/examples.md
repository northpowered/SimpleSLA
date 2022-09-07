# Examples

## Typical full config file

```yaml
Server:
  bind_address: '0.0.0.0'
  port: 8800
  refresh_time: 2

Global:
  unit: 'ms'

Local:
  src_addr: '0.0.0.0' 
  timeout: 1
  ttl: 64
  size: 56

Devices:
  - name: 'RT_1'
    type: 'cisco'
    transport: 'telnet'
    address: '192.168.0.1'
    username: 'user'
    password: 'password'
    port: 23
  - name: 'RT_2'
    type: 'juniper'
    transport: 'ssh'
    address: '192.168.0.9'
    username: 'user'
    password: 'password'
    port: 22


Policies:
  - name: mypolicy
    max_rtt: 0.9

ServicesGroups:
  - name: mygroup
    device: 'RT_1'
    services:
      - name: serv1
        target: '10.26.6.3'
        delay: 3
        policy: mypolicy
      - name: serv2
        target: '10.26.6.9'
        delay: 8

Services:
  - name: 'service01'
    device: 'simplesla-local'
    target: '192.168.0.24'
    delay: 16
  - name: 'service02'
    device: 'RT_2'
    target: '16.2.6.9'
    delay: 5
    policy: mypolicy
```