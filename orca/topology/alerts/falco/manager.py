from orca.topology import manager
from orca.topology.alerts import probe


class ProbeManager(manager.ProbeManager):

    def initialize_probes(self):
        return [probe.Probe(graph=self._graph, origin='falco', kind='alert')]
