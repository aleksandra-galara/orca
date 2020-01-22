import cotyledon

from orca.graph import drivers as graph_drivers
from orca.graph.graph import Graph
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import probe as k8s_probe
from orca.topology.probes import probe
from orca.topology.probes.k8s import pod
from orca.topology.probes.k8s import service
from orca.topology.probes.k8s import replica_set
from orca.topology.probes.k8s import deployment
from orca.topology.probes.k8s import node
from orca.topology.probes.k8s import secret
from orca.topology.probes.k8s import config_map
from orca.topology.probes import linker


class Manager(cotyledon.ServiceManager):

    def __init__(self):
        super().__init__()
        graph = self._init_graph()
        self._add_k8s_probes(graph)

    def _init_graph(self):
        # TODO: read graph backend from config
        graph_client = graph_drivers.ClientFactory.get_client('neo4j')
        return Graph(graph_client)

    def _add_k8s_probes(self, graph):
        k8s = k8s_client.ClientFactory.get_client()

        # linkers
        pod_to_service = linker.Linker(
            kind_a='pod',
            kind_b='service',
            graph=graph,
            matcher=pod.PodToServiceMatcher())

        pod_to_replica_set = linker.Linker(
            kind_a='pod',
            kind_b='replica_set',
            graph=graph,
            matcher=pod.PodToReplicaSetMatcher())

        pod_to_node = linker.Linker(
            kind_a='pod',
            kind_b='node',
            graph=graph,
            matcher=pod.PodToNodeMatcher())

        replica_set_to_deployment = linker.Linker(
            kind_a='replica_set',
            kind_b='deployment',
            graph=graph,
            matcher=replica_set.ReplicaSetToDeploymentMatcher())

        config_map_to_pod = linker.Linker(
            kind_a='config_map',
            kind_b='pod',
            graph=graph,
            matcher=config_map.ConfigMapToPodMatcher())

        secret_to_pod = linker.Linker(
            kind_a='secret',
            kind_b='pod',
            graph=graph,
            matcher=secret.SecretToPodMatcher())

        node_to_cluster = linker.Linker(
            kind_a='node',
            kind_b='cluster',
            graph=graph,
            matcher=node.NodeToClusterMatcher())

        # probes
        pod_probe = k8s_probe.Probe(
            kind='pod',
            extractor=pod.PodExtractor(),
            linkers=[pod_to_service, pod_to_replica_set, pod_to_node, config_map_to_pod,
                     secret_to_pod],
            graph=graph,
            k8s_client=k8s_client.ResourceProxy.get(k8s, 'pod'))

        service_probe = k8s_probe.Probe(
            kind='service',
            extractor=service.ServiceExtractor(),
            linkers=[pod_to_service],
            graph=graph,
            k8s_client=k8s_client.ResourceProxy.get(k8s, 'service'))

        replica_set_probe = k8s_probe.Probe(
            kind='replica_set',
            extractor=replica_set.ReplicaSetExtractor(),
            linkers=[pod_to_replica_set, replica_set_to_deployment],
            graph=graph,
            k8s_client=k8s_client.ResourceProxy.get(k8s, 'replica_set'))

        deployment_probe = k8s_probe.Probe(
            kind='deployment',
            extractor=deployment.DeploymentExtractor(),
            linkers=[replica_set_to_deployment],
            graph=graph,
            k8s_client=k8s_client.ResourceProxy.get(k8s, 'deployment'))

        config_map_probe = k8s_probe.Probe(
            kind='config_map',
            extractor=config_map.ConfigMapExtractor(),
            linkers=[config_map_to_pod],
            graph=graph,
            k8s_client=k8s_client.ResourceProxy.get(k8s, 'config_map'))

        secret_probe = k8s_probe.Probe(
            kind='secret',
            extractor=secret.SecretExtractor(),
            linkers=[secret_to_pod],
            graph=graph,
            k8s_client=k8s_client.ResourceProxy.get(k8s, 'secret'))

        node_probe = k8s_probe.Probe(
            kind='node',
            extractor=node.NodeExtractor(),
            linkers=[pod_to_node, node_to_cluster],
            graph=graph,
            k8s_client=k8s_client.ResourceProxy.get(k8s, 'node'))

        subprobes = [pod_probe, service_probe, replica_set_probe, deployment_probe,
                     config_map_probe, secret_probe, node_probe]

        for subprobe in subprobes:
            self.add(probe.ProbeService, workers=1, args=(subprobe,))
