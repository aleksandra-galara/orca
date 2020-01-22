from orca.topology.probes.k8s import extractor
from orca.topology.probes.k8s import linker


class NodeExtractor(extractor.Extractor):

    def extract_kind(self, entity):
        return 'node'

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        return properties


class NodeToClusterMatcher(linker.Matcher):

    def are_linked(self, pod, node):
        return True
