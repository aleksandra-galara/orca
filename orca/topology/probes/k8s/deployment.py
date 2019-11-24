from orca.common import logger
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import probe

log = logger.get_logger(__name__)


class DeploymentProbe(probe.Probe):

    def run(self):
        log.info("Starting K8S watch on resource: deployment")
        watch = k8s_client.ResourceWatch(self._client.AppsV1Api(), 'deployment')
        watch.add_handler(DeploymentHandler(self._graph))
        watch.run()


class DeploymentHandler(probe.K8SResourceHandler):

    def _extract_properties(self, obj):
        id = obj.metadata.uid
        properties = {}
        properties['name'] = obj.metadata.name
        properties['namespace'] = obj.metadata.namespace
        return (id, 'deployment', properties)
