# Installation

## With Docker

The most convinient way to use SimpleSLA is Docker image. Image can be used as a single container right with Docker or, for example, in group of services with Docker Compose

To download the image, execute this command:
    
    docker pull ghcr.io/northpowered/simple-sla:latest

Then run the downloaded image

    docker run --name simple-sla ghcr.io/northpowered/simple-sla:latest

> Do not forget to create `volume` for config file and expose `port` for HTTP server

## With Docker Compose

```yaml
version: '3.5'

networks:
  simplesla-network:
    driver: bridge

services:
  simple-sla:
    image: "ghcr.io/northpowered/simple-sla:latest"
    container_name: simple-sla
    restart: always
    environment:
      - SSLA_LL=INFO
    ports:
     - "8800:8800"
    volumes:
      - ./config.yml:/app/config.yml
    networks:
      - simplesla-network
```

