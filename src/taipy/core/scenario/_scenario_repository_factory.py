# Copyright 2022 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from typing import Type

from .._repository._repository_factory import _RepositoryFactory
from ..common._utils import _load_fct
from ._scenario_fs_repository import _ScenarioFSRepository
from ._scenario_repository import _ScenarioRepository


class _ScenarioRepositoryFactory(_RepositoryFactory):
    @classmethod
    def _build_repository(cls) -> Type[_ScenarioRepository]:  # type: ignore
        if cls._using_enterprise():
            factory = _load_fct(
                cls._TAIPY_ENTERPRISE_CORE_MODULE + ".scenario._scenario_repository_factory",
                "_ScenarioRepositoryFactory",
            )
            return factory._build_repository()  # type: ignore
        return _ScenarioFSRepository()