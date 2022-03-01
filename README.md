# SimpleSLA

Easy SLA control system for distribiuted networks

## Usage

python3 main.py [-h] -c CONFIG [-l {DEBUG,INFO,WARNING,ERROR}]
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
