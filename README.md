# SimpleSLA

Easy SLA control system for distribiuted networks

Obtain RTT value from devices, check policy and export all of this to Prometeus

Supported devices:
  - Cisco
  - Juniper
  - Eltex (ESR series)
  - MT M716

## Usage
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
### Install:

```bash
    pip install -r requirements.txt
    python3 main.py  -c config.yml
```
### Docker

```bash
    docker build -t simplesla:yourtag .
    docker run -p "8800:8800" simplesla:yourtag
```

