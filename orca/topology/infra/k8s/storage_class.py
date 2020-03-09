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

from orca.topology.infra.k8s import extractor


class StorageClassExtractor(extractor.Extractor):

    def get_kind(self):
        return 'storage_class'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['provisioner'] = entity.provisioner
        properties['reclaim_policy'] = entity.reclaim_policy
        properties['parameters'] = entity.parameters.copy()
        return properties