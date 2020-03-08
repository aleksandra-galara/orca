import cotyledon

from orca.graph import drivers as graph_drivers
from orca.graph.graph import Graph
from orca.topology import linker, probe


class Manager(cotyledon.ServiceManager):

    def __init__(self):
        super().__init__()

    def initialize(self):
        graph = self._init_graph()
        linker_dispatcher = linker.Dispatcher()
        graph.add_listener(linker_dispatcher)
        probe_managers = []

        from orca.topology.infra.k8s import manager as k8s
        probe_managers.append(k8s.ProbeManager(graph))

        from orca.topology.infra.istio import manager as istio
        probe_managers.append(istio.ProbeManager(graph))

        from orca.topology.infra.kiali import manager as kiali
        probe_managers.append(kiali.ProbeManager(graph))

        from orca.topology.alerts.prometheus import manager as prom
        probe_managers.append(prom.ProbeManager(graph))

        from orca.topology.alerts.elastalert import manager as es
        probe_managers.append(es.ProbeManager(graph))

        from orca.topology.alerts.falco import manager as falco
        probe_managers.append(falco.ProbeManager(graph))

        for probe_manager in probe_managers:
            for probe_inst in probe_manager.initialize_probes():
                self.add(probe.ProbeService, workers=1, args=(probe_inst,))

            for linker_inst in probe_manager.initialize_linkers():
                linker_dispatcher.add_linker(linker_inst)

    def _init_graph(self):
        # TODO: read graph backend from config
        graph_client = graph_drivers.DriverFactory.get('neo4j')
        return Graph(graph_client)


class ProbeManager(object):

    def __init__(self, graph):
        self._graph = graph

    def initialize_probes(self):
        """Initializes all probes for given origin."""
        return []

    def initialize_linkers(self):
        """Initializes all linkers for given origin."""
        return []
