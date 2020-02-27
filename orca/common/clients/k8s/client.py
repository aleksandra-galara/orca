import abc

import addict as dictlib
from kubernetes import client, config, watch


class ClientFactory(object):

    @staticmethod
    def get():
        config.load_incluster_config()
        return client


class ResourceProxy(object):

    def __init__(self, list_fn):
        self._list_fn = list_fn

    def get_all(self):
        return self._list_fn().items

    def watch(self, handler):
        for event in self._watch_resource():
            event_type, event_object = event['type'], event['object']
            if event_type == "ADDED":
                handler.on_added(event_object)
            elif event_type == "MODIFIED":
                handler.on_updated(event_object)
            elif event_type == "DELETED":
                handler.on_deleted(event_object)
            else:
                raise Exception("Unknown event type '%s': %s" % (event_type, event_object))

    def _watch_resource(self):
        return watch.Watch().stream(self._list_fn)


class CustomResourceProxy(ResourceProxy):

    def __init__(self, list_fn, group, version, plural):
        super().__init__(list_fn)
        self._group = group
        self._version = version
        self._plural = plural

    def get_all(self):
        items = self._list_fn(self._group, self._version, self._plural)['items']
        return [self._extract_item(item) for item in items]

    def _watch_resource(self):
        for event in watch.Watch().stream(self._list_fn, self._group, self._version, self._plural):
            event['object'] = self._extract_item(event.pop('object'))
            yield event

    def _extract_item(self, item):
        return dictlib.Dict(item)


class ResourceProxyFactory(object):

    @staticmethod
    def get(k8s_client, kind):
        if kind == 'pod':
            return ResourceProxy(
                k8s_client.CoreV1Api().list_pod_for_all_namespaces)
        elif kind == 'service':
            return ResourceProxy(
                k8s_client.CoreV1Api().list_service_for_all_namespaces)
        elif kind == 'config_map':
            return ResourceProxy(
                k8s_client.CoreV1Api().list_config_map_for_all_namespaces)
        elif kind == 'secret':
            return ResourceProxy(
                k8s_client.CoreV1Api().list_secret_for_all_namespaces)
        elif kind == 'node':
            return ResourceProxy(
                k8s_client.CoreV1Api().list_node)
        elif kind == 'deployment':
            return ResourceProxy(
                k8s_client.AppsV1Api().list_deployment_for_all_namespaces)
        elif kind == 'stateful_set':
            return ResourceProxy(
                k8s_client.AppsV1Api().list_stateful_set_for_all_namespaces)
        elif kind == 'daemon_set':
            return ResourceProxy(
                k8s_client.AppsV1Api().list_daemon_set_for_all_namespaces)
        elif kind == 'replica_set':
            return ResourceProxy(
                k8s_client.ExtensionsV1beta1Api().list_replica_set_for_all_namespaces)
        else:
            raise Exception("Unknown kind %s" % kind)


class EventHandler(abc.ABC):

    @abc.abstractmethod
    def on_added(self, event_object):
        """Triggered when a K8S resource is added."""

    @abc.abstractmethod
    def on_updated(self, event_object):
        """Triggered when a K8S resource is updated."""

    @abc.abstractmethod
    def on_deleted(self, event_object):
        """Triggered when a K8S resource is deleted."""
