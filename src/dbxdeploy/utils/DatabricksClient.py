import re

import databricks_cli.sdk.service as services
from databricks_cli.sdk import ApiClient


def camel_to_snake(name):
    s = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def _get_services():
    for service_name, service in services.__dict__.items():
        if "Service" in service_name:
            snake_name = camel_to_snake(service_name.replace("Service", ""))
            yield service_name, snake_name, service


class DatabricksClient:
    jobs: services.JobsService
    cluster: services.ClusterService
    policy: services.PolicyService
    managed_library: services.ManagedLibraryService
    dbfs: services.DbfsService
    workspace: services.WorkspaceService
    secret: services.SecretService
    groups: services.GroupsService
    token: services.TokenService
    instance_pool: services.InstancePoolService
    delta_pipelines: services.DeltaPipelinesService
    repos: services.ReposService

    def __init__(self, client: ApiClient):
        self.client = client

        for _, snake_name, service in _get_services():
            setattr(self, snake_name, service(self.client))
