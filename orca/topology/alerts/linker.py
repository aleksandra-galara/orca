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


from orca.topology import linker


class Linker(linker.Linker):

    """Base class for alert linkers."""

    def _get_current_links(self, node):
        return self._graph.get_node_links(node)

    def _get_linked_nodes(self, alert_node):
        source_mapping = alert_node.properties.source_mapping
        return self._graph.get_nodes(
            kind=source_mapping.kind, properties=source_mapping.properties)


class Matcher(linker.Matcher):

    """Base class for alert matchers."""


class AlertToSourceMatcher(Matcher):

    """Generic matcher for links between Alert and source objects."""

    def are_linked(self, alert, obj):
        source_mapping = alert.properties.source_mapping
        if source_mapping.kind == obj.kind:
            return all(item in obj.properties.items() for item in source_mapping.properties.items())
        return False
