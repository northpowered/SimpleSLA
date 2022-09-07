[![CodeFactor](https://www.codefactor.io/repository/github/northpowered/simplesla/badge)](https://www.codefactor.io/repository/github/northpowered/simplesla)
[![Docker Image CI/CD](https://github.com/northpowered/SimpleSLA/actions/workflows/docker-image.yml/badge.svg)](https://github.com/northpowered/SimpleSLA/actions/workflows/docker-image.yml)
# SimpleSLA

Easy SLA control system for distribiuted networks

Full documentation available [here](https://northpowered.github.io/SimpleSLA/)

Obtain RTT value from devices, check policy and export all of this to Prometeus

Available ways to collect RTT:

  - Directly from host with SimpleSLA (*simplesla-local* in 'device' field)
  - Between two remote devices (SSH or telnet to closest device)

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
