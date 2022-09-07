# Configuration structure

All configuration options defined in one YAML file, ex `config.yaml`, that has some sections, represented below.

## *Server*

Settings for a HTTP server of Prometheus endpoint 

```yaml
Server:
  bind_address: '0.0.0.0'
  port: 8800
  refresh_time: 20
```
**`bind address`** - Ipv4 or DSN for binding http server with metrics

**`port`** - Port for http server

**`refresh_time`** (seconds) - Time of updating data in prometheus endpoint. This is independent from collectors of these metrics

## *Global*

Global settings for metric collectors

```yaml
Global:
  unit: 'ms'
```
**`unit`** - Unit of Round-Trip-Time (RTT) in collected metrics

## *Local*

Settings of `simplesla-local` device for ICMP checks

```yaml
Local:
  src_addr: '0.0.0.0' 
  timeout: 1
  ttl: 64
  size: 56
```
**`src_addr`** - Source address for ICMP requests from SimpleSLA

**`timeout`** (seconds) - Timeout for ICMP requests

**`ttl`** - TTL for outgoing packets

**`size`** (bytes) - Payload size of ICMP packets

## *Devices*

List of registered devices

```yaml
Devices:
  - name: 'my_device'
    type: 'cisco'
    transport: 'ssh'
    address: '192.168.0.1'
    username: 'user'
    password: 'password'
    port: 22
```
**`name`** - Unique name of device, using in metric`s labels

**`type`** - Type of device, see full list of supported devices [here](../supported_devices.md)

**`transport`** - protocol to connect to the device, `ssh` and `telnet` are supported now

**`address`** - IPv4 or DSN of the device

**`username`** - Username to login to the device

**`password`** - Password for the account

**`port`** - Port number for connection

## *Policies*

List of policies to define status of service

```yaml
Policies:
  - name: mypolicy
    max_rtt: 0.15
```

**`name`** - Unique name of the policy

**`max_rtt`** - Max value of RTT to change service status

## *Services*

List of single services for metric collection

```yaml
Services:
  - name: 'my_service01'
    device: 'simplesla-local'
    target: '192.168.0.10'
    delay: 3
    policy: mypolicy
  - name: 'my_service02'
    device: 'my_device'
    target: '10.35.45.91'
    delay: 7
```

**`name`** - Unique name of the service, using on metric`s labels

**`device`** - Name of the source device. Device MUST be defined in [Devices](index.md#devices) section

**`target`** - IPv4 or DSN as a destionation for checks

**`delay`** (seconds) - Pause between checking sessions

**`policy`** (*OPTIONAL*) - If using, MUST be defined in [Policies](index.md#policies) section

## *ServicesGroups*

```yaml
ServicesGroups:
  - name: mygroup
    device: 'my_device'
    delay: 3
    policy: mypolicy
    services:
      - name: serv1
        target: '10.71.206.2'
        policy: mypolicy
      - name: serv2
        target: '10.71.206.75'
        delay: 3
```

**`name`** - Unique name of service group

**`device`** - Device for all sub services

**`delay`** (seconds) - Delay for all sub services

**`policy`** - Policy for all sub services

**`services`** - List of sub services. `delay` and `policy` can be overwritten