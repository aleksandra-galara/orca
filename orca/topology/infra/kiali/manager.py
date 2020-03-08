from orca.common.clients.kiali import client as kiali
from orca.topology import manager
from orca.topology.infra.kiali import probe


class ProbeManager(manager.ProbeManager):

    def initialize_probes(self):
        kiali_client = self._init_kiali_client()
        return [
            probe.Probe(graph=self._graph, kiali_client=kiali_client)]

    def _init_kiali_client(self):
        return kiali.KialiClient.get(
            "http://kiali.istio-system:20001", username="admin", password="admin")
