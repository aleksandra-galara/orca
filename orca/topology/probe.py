# Copyright 2020 OpenRCA Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import time

import cotyledon

from orca import exceptions
from orca.common import logger

log = logger.get_logger(__name__)


class ProbeService(cotyledon.Service):

    def __init__(self, service_id, probe):
        super().__init__(service_id)
        self._service_id = service_id
        self._probe = probe

    def run(self):
        self._probe.run()


class Probe(abc.ABC):

    """Base class for entity probes."""

    def __init__(self, graph):
        super().__init__()
        self._graph = graph

    @abc.abstractmethod
    def run(self):
        """Starts entity probe."""


class PullProbe(Probe):

    """Periodically pulls all entities from the upstream into the graph."""

    def __init__(self, graph, upstream_proxy, extractor, synchronizer):
        super().__init__(graph)
        self._extractor = extractor
        self._upstream_proxy = upstream_proxy
        self._synchronizer = synchronizer

    def run(self):
        while True:
            extended_kind = self._extractor.get_extended_kind()
            log.info("Starting sync for entity: %s", extended_kind)
            self._synchronize()
            log.info("Finished sync for entity: %s", extended_kind)
            time.sleep(60)

    def _synchronize(self):
        nodes_in_graph = self._get_nodes_in_graph()
        upstream_nodes = self._get_upstream_nodes()
        self._synchronizer.synchronize(nodes_in_graph, upstream_nodes)

    def _get_nodes_in_graph(self):
        return self._graph.get_nodes(
            origin=self._extractor.get_origin(), kind=self._extractor.get_kind())

    def _get_upstream_nodes(self):
        entities = self._upstream_proxy.get_all()
        upstream_nodes = []
        for entity in entities:
            try:
                node = self._extractor.extract(entity)
                upstream_nodes.append(node)
            except exceptions.OrcaError as ex:
                log.warning("Error while processing an entity: %s", ex)
        return upstream_nodes


class UpstreamProxy(abc.ABC):

    @abc.abstractmethod
    def get_all(self):
        """Retrieves all entities from the upstream."""
