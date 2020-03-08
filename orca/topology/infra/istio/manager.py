from orca.common.clients.istio import client as istio
from orca.common.clients.k8s import client as k8s
from orca.topology import linker
from orca.topology.infra.istio import (destination_rule, gateway,
                                       virtual_service)
from orca.topology.infra.k8s import manager, probe


class ProbeManager(manager.ProbeManager):

    def initialize_probes(self):
        k8s_client = self._init_k8s_client()
        return [
            probe.Probe(
                graph=self._graph,
                extractor=virtual_service.VirtualServiceExtractor(),
                k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'virtual_service')),
            probe.Probe(
                graph=self._graph,
                extractor=destination_rule.DestinationRuleExtractor(),
                k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'destination_rule')),
            probe.Probe(
                graph=self._graph,
                extractor=gateway.GatewayExtractor(),
                k8s_client=istio.ResourceProxyFactory.get(k8s_client, 'gateway'))]

    def initialize_linkers(self):
        return [
            linker.Linker(
                source_kind='virtual_service',
                target_kind='gateway',
                graph=self._graph,
                matcher=virtual_service.VirtualServiceToGatewayMatcher()),
            linker.Linker(
                source_kind='virtual_service',
                target_kind='service',
                graph=self._graph,
                matcher=virtual_service.VirtualServiceToServiceMatcher()),
            linker.Linker(
                source_kind='destination_rule',
                target_kind='service',
                graph=self._graph,
                matcher=destination_rule.DestinationRuleToServiceMatcher())]
