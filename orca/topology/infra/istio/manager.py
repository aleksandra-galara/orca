from orca.common.clients.istio import client as istio
from orca.common.clients.k8s import client as k8s
from orca.topology import linker
from orca.topology.infra.istio import (destination_rule, gateway,
                                       virtual_service)
from orca.topology.infra.k8s import probe


def initialize_probes(graph):
    k8s_client = k8s.ClientFactory.get()
    return [
        probe.Probe(
            extractor=virtual_service.VirtualServiceExtractor(),
            graph=graph,
            k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'virtual_service')),
        probe.Probe(
            extractor=destination_rule.DestinationRuleExtractor(),
            graph=graph,
            k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'destination_rule')),
        probe.Probe(
            extractor=gateway.GatewayExtractor(),
            graph=graph,
            k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'gateway'))]


def initialize_linkers(graph):
    return [
        linker.Linker(
            source_kind='virtual_service',
            target_kind='gateway',
            graph=graph,
            matcher=virtual_service.VirtualServiceToGatewayMatcher()),
        linker.Linker(
            source_kind='virtual_service',
            target_kind='service',
            graph=graph,
            matcher=virtual_service.VirtualServiceToServiceMatcher()),
        linker.Linker(
            source_kind='destination_rule',
            target_kind='service',
            graph=graph,
            matcher=destination_rule.DestinationRuleToServiceMatcher())]
