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

import copy
import json

import arango

from orca.graph import graph
from orca.graph.drivers import driver


class ArangoDBDriver(driver.Driver):

    """Arango Graph DB client."""

    def __init__(self, host, port, database, username=None, password=None):
        super().__init__()
        self._host = host
        self._port = port
        self._database = database
        self._username = username
        self._password = password
        self.__client = None
        self.__graph = None

    @property
    def _client(self):
        if not self.__client:
            self.__client = self._initialize_client()
        return self.__client

    @property
    def _graph(self):
        if not self.__graph:
            self.__graph = self._initialize_graph()
        return self.__graph

    @property
    def _nodes(self):
        return self._graph.vertex_collection('nodes')

    @property
    def _links(self):
        return self._graph.edge_collection('links')

    def get_nodes(self, origin=None, kind=None, properties=None):
        query = {}
        if origin:
            query['origin'] = origin
        if kind:
            query['kind'] = kind
        if properties:
            query.update(properties)
        raw_nodes = self._nodes.find(query)
        return [self._build_node(node) for node in raw_nodes]

    def get_node(self, node_id):
        raw_node = self._nodes.get(node_id)
        if raw_node:
            return self._build_node(raw_node)

    def add_node(self, node):
        document = self._build_node_document(node)
        self._nodes.insert(document)

    def update_node(self, node):
        document = self._build_node_document(node)
        self._nodes.update(document)

    def delete_node(self, node):
        self._nodes.delete(self._build_key(node))

    def get_links(self, properties):
        raw_links = self._links.find(properties)
        return [self._build_link(link) for link in raw_links]

    def get_link(self, link_id):
        raw_link = self._links.get(link_id)
        if raw_link:
            return self._build_link(raw_link)

    def add_link(self, link):
        document = self._build_link_document(link)
        self._links.insert(document)

    def update_link(self, link):
        document = self._build_link_document(link)
        self._links.update(document)

    def delete_link(self, link):
        self._links.delete(self._build_key(link))

    def get_node_links(self, node, origin=None, kind=None):
        source_id = self._build_id('nodes', node)
        raw_links = self._links.edges(source_id, direction='out')['edges']
        return [self._build_link(link) for link in raw_links]

    def _initialize_client(self):
        return arango.ArangoClient(hosts=self._get_db_uri())

    def _get_db_uri(self):
        return "http://%s:%s" % (self._host, self._port)

    def _initialize_graph(self):
        sys_db = self._use_database('_system')

        if not sys_db.has_database(self._database):
            sys_db.create_database(self._database)
        db = self._use_database(self._database)

        if not db.has_graph('graph'):
            db.create_graph('graph')
        graph = db.graph('graph')

        if not graph.has_vertex_collection('nodes'):
            graph.create_vertex_collection('nodes')

        if not graph.has_edge_definition('links'):
            graph.create_edge_definition(
                edge_collection='links',
                from_vertex_collections=['nodes'],
                to_vertex_collections=['nodes'])
        return graph

    def _use_database(self, database):
        return self._client.db(
            database,username=self._username, password=self._password)

    def _build_node_document(self, node):
        document = copy.deepcopy(node.properties)
        document['origin'] = node.origin
        document['kind'] = node.kind
        document['_key'] = self._build_key(node)
        return document

    def _build_link_document(self, link):
        document = copy.deepcopy(link.properties)
        document['_key'] = self._build_key(link)
        document['_from'] = self._build_id('nodes', link.source)
        document['_to'] = self._build_id('nodes', link.target)
        return document

    def _build_key(self, graph_obj):
        return str(graph_obj.id)

    def _build_id(self, collection, graph_obj):
        return "%s/%s" % (collection, graph_obj.id)

    def _get_key_from_id(self, document_id):
        return document_id.split('/')[1]

    def _build_node(self, raw_node):
        node_id = raw_node.pop('_key')
        properties = raw_node
        for key in ['_id', '_rev']:
            properties.pop(key)
        origin = properties.pop('origin')
        kind = properties.pop('kind')
        return graph.Node(node_id, properties, origin, kind)

    def _build_link(self, raw_link):
        link_id = raw_link.pop('_key')
        properties = raw_link
        for key in ['_id', '_rev']:
            properties.pop(key)
        source_key = self._get_key_from_id(properties.pop('_from'))
        target_key = self._get_key_from_id(properties.pop('_to'))
        source_node = self.get_node(source_key)
        target_node = self.get_node(target_key)
        return graph.Link(link_id, properties, source_node, target_node)
