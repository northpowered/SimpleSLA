from typing import Union

class Policy():
    def __init__(self, name: str, max_rtt:Union[int, float]) -> None:
        self.name = name
        self.max_rtt = max_rtt

    def is_warn(self, rtt:Union[int, float]):
        return float(rtt) >= float(self.max_rtt)

