[![CodeFactor](https://www.codefactor.io/repository/github/northpowered/simplesla/badge)](https://www.codefactor.io/repository/github/northpowered/simplesla)
[![Docker Image CI/CD](https://github.com/northpowered/SimpleSLA/actions/workflows/docker-image.yml/badge.svg)](https://github.com/northpowered/SimpleSLA/actions/workflows/docker-image.yml)
# SimpleSLA

Easy SLA control system for distribiuted networks

Obtain RTT value from devices, check policy and export all of this to Prometeus

Available ways to collect RTT:

  - Directly from host with SimpleSLA (*simplesla-local* in 'device' field)
  - Between two remote devices (SSH or telnet to closest device)

Supported devices:
  - Cisco
  - Juniper
  - Eltex (ESR series)
  - MT M716
  - Potok KM-122

TODO:
  - Extending devices support
  - Export data via logs (Loki way)
  - Authentication via ssh with keys
  - Logic for global_unit parameter
  - Extend policies with severeties
  - Async server
  - Refactoring
  - Tests

## Usage

### Running from source
> pip install -r requirements.txt

> python3 main.py  -c config.yml
### In CLI mode
```bash
python3 main.py -c CONFIG

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to configuration yaml file
  -v {DEBUG,INFO,WARNING,ERROR}, --verbose {DEBUG,INFO,WARNING,ERROR}
                        Logging level
  -l LOG_DEST, --log-dest LOG_DEST
                        Logging path {stdout,FILE}
  --version             show programs version number and exit
```
### Using docker image
> docker pull ghcr.io/northpowered/simple-sla:latest

> docker run --name simple-sla ghcr.io/northpowered/simple-sla:latest
## SLA statuses

| Status      | Int value   | Recommended color | Description |
| ----------- | ----------- |------------------ |------------ |
| NoData      | 0           | Black             | No recieved data or parcing error |
| Normal      | 1           | Green             | Target is available and RTT less then policy |
| Warning     | 2           | Yellow            | Target is available and RTT bigger then policy |
| Error       | 3           | Red               | Target is unavailable |
| OutOfService| 4           | Green             | Target is available and policy was not defined |

## Configuration

All config is represented in YAML format

#### Section *server*
  ```yaml
server:
    bind_address: '0.0.0.0'  #[STRING] Ipv4 for binding http server with Prometheus endpoint
    port: 8800 #[INT] Port for binding http server, be carefull about permissions for different port
    refresh_time: 2 #[INT] Prometheus endpoint update time, in seconds

  ```
#### Section *global*
  ```yaml
  global:
    unit: 'ms' #[STRING] global unit of RTT [in progress]
  ```

#### Section *local*
Configuration of *simplesla-local* device
  ```yaml
  local:
    src_addr: '0.0.0.0' #[STRING] Source ping address
    timeout: 1 #[INT] ICMP timeout in seconds
    ttl: 64 #[INT] Max TTL for ICMP
    size: 56 #[INT] Payload size in bytes
  ```

#### Section *devices*
  ```yaml
  devices:
    - name: 'RT' #[STRING] unique name of device
      type: 'cisco' #[STRING] type of device, see supported device types
      transport: 'telnet' #[STRING] telnet or ssh
      address: '10.10.10.1' #[STRING] Device address 
      username: 'admin' #[STRING] Username (ssh/telnet) 
      password: 'cisco' #[STRING] Plaintext password (ssh/telnet) 
      port: 23 #[INT] Connection port for (ssh/telnet), default (22/23)
  ```
#### Section *policies*
  ```yaml
  policies:
    - name: mypolicy #[STRING] unique name of policy
      max_rtt: 0.15 #[FLOAT] Max RTT in seconds
  ```
#### Section *services*
  ```yaml
  services:
    - name: 'service01' #[STRING] unique name of service
      device: 'simplesla-local' #[STRING] Target device, device MUST exist in devices section, or simplesla-local
      target: '192.168.0.2' #[STRING] ICMP target, which will be checked from device
      delay: 3 #[INT] Check delay, in seconds
      policy: mypolicy #[STRING] OPTIONAL police name, policy MUST exist in policies section
    - name: 'sevice02'
      device: 'RT'
      target: '10.10.10.2'
      delay: 4
  ```
#### Services groups
> To avoid multiple connections to one device, you can group your services, which should
be checked from one point
```yaml
ServicesGroups:
  - name: mygroup
    device: mydevice
    policy: policy_for_all_subservices_without_own_policy
    delay: 4  #the same for delay
    services:
      - name: serv1
        target: '192.168.0.6'
        policy: my_own_policy
      - name: serv2
        target: '10.3.5.3'
        delay: 3
```