# SimpleSLA

Easy SLA control system for distribiuted networks

## Usage

usage: main.py [-h] -c CONFIG [-v {DEBUG,INFO,WARNING,ERROR}] [-l LOG_DEST] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to configuration yaml file
  -v {DEBUG,INFO,WARNING,ERROR}, --verbose {DEBUG,INFO,WARNING,ERROR}
                        Logging level
  -l LOG_DEST, --log-dest LOG_DEST
                        Logging path {stdout,FILE}
  --version             show program's version number and exit
### Overview:

```bash
    pip install -r requirements.txt
    python3 main.py  -c config.yml -l {DEBUG,INFO,WARNING,ERROR}
```
### Docker

```bash
    docker build -t simplesla:yourtag .
    docker run -p "8800:8800" simplesla:yourtag
```

### Docker-compose

At first, build the image with the command above and edit docker-compose.yml file

```bash
docker-compose up
```
