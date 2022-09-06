# Configuration structure

All configuration options defined in one YAML file, ex `config.yaml`, that has some sections, represented below.

## *Server*

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
```yaml
Global:
  unit: 'ms'
```
**`unit`** - Unit of Round-Trip-Time (RTT) in collected metrics

## *Local*
```yaml
Local:
  src_addr: '0.0.0.0' 
  timeout: 1
  ttl: 64
  size: 56
```
