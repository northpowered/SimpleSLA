from prometheus_client.core import GaugeMetricFamily, REGISTRY
from sla.service import SERVICE_RESULTS
from sla.logger import LG


class Collector(object):
    def __init__(self) -> None:
        super().__init__()

    def collect(self):
        for key in SERVICE_RESULTS.keys():
            service = SERVICE_RESULTS[key]
            c = GaugeMetricFamily(
                "s_rtt_" + str(key), "Service metrics", labels=["name"]
            )
            rtt = service["rtt"]
            if not isinstance(rtt, (int, float)):  # downservice should have 0 rtt
                rtt = 0
            c.add_metric([str(key) + "_rtt"], rtt)
            c.add_metric([str(key) + "_status"], service["status"])
            yield c
