"""
Continuous Deployment Helper module
"""

# Copyright 2020 Croix Bleue du Québec

# This file is part of python-devops-sccs.

# python-devops-sccs is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# python-devops-sccs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with python-devops-sccs.  If not, see <https://www.gnu.org/licenses/>.

from ..errors import TriggerCdNotSupported, TriggerCdReadOnly, TriggerCdEnvUnsupported, TriggerCdVersionUnsupported, TriggerCdVersionAlreadyDeployed

def trigger_prepare(continuous_deployment, versions_available, repository, environment, version):
    """
    Check conformity to trigger a deployment
    Extract involved configurations from the global config

    Args:
        continuous_deployment(typing.cd.EnvironmentConfig): The configuration
        versions_available(list(typing.cd.Available)): List of versions available 
        repository(str): the repository name
        environment(str): the environment (eg: production, development, qa, ...)
        version(str): version to deploy

    Returns:
        typing.cd.EnvironmentConfig, typing.cd.Available: Environment configuration target, Available Deployment target
    """

    if continuous_deployment.readonly:
        raise TriggerCdReadOnly(repository, environment)

    if continuous_deployment.version == version:
        raise TriggerCdVersionAlreadyDeployed(repository, environment, version)

    for available in versions_available:
        if available.version == version:
            return continuous_deployment, available

    raise TriggerCdVersionUnsupported(repository, version)

def trigger_not_supported(repository, environment):
    """Trigger Continuous Deployment is not supported for this repository/environment"""
    raise TriggerCdEnvUnsupported(repository, environment)
