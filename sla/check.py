from ping3 import ping, verbose_ping


def check(service):

    a = ping(service['address'], timeout=1, unit='ms', src_addr='0.0.0.0', interface='eno1', ttl=64, size=56) 
    return a
    