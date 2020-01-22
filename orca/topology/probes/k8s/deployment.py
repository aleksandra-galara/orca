from orca.topology.probes.k8s import extractor


class DeploymentExtractor(extractor.Extractor):

    def extract_kind(self, entity):
        return 'deployment'

    def extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['selector'] = entity.spec.selector.match_labels
        return properties
