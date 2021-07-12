from ocp_resources.mtv import MTV
from ocp_resources.resource import NamespacedResource


class Plan(NamespacedResource, MTV):
    """
    Migration Tool for Virtualization (MTV) Plan Resource.

    Args:
        source_provider_name (str): MTV Source Provider CR name.
        source_provider_namespace (str): MTV Source Provider CR namespace.
        destination_provider_name (str): MTV Destination Provider CR name.
        destination_provider_namespace (str): MTV Destination Provider CR namespace.
        storage_map_name (str): MTV StorageMap CR name.
        storage_map_namespace (str): MTV StorageMap CR namespace.
        network_map_name (str): MTV NetworkMap CR name.
        network_map_namespace (str): MTV NetworkMap CR CR namespace.
        virtual_machines_list (list): A List of dicts, each contain the name Or id of the source Virtual Machines to migrate.
            Example: [ { "id": "vm-id-x" }, { "name": "vm-name-x" } ]
        warm_migration (bool, default: False): Warm (True) or Cold (False) migration.
    """


    def __init__(
        self,
        name,
        namespace,
        source_provider_name=None,
        source_provider_namespace=None,
        destination_provider_name=None,
        destination_provider_namespace=None,
        storage_map_name=None,
        storage_map_namespace=None,
        network_map_name=None,
        network_map_namespace=None,
        virtual_machines_list=None,
        target_namespace=None,
        warm_migration=False,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.source_provider_name = source_provider_name
        self.source_provider_namespace = source_provider_namespace
        self.destination_provider_name = destination_provider_name
        self.destination_provider_namespace = destination_provider_namespace
        self.storage_map_name = storage_map_name
        self.storage_map_namespace = storage_map_namespace
        self.network_map_name = network_map_name
        self.network_map_namespace = network_map_namespace
        self.virtual_machines_list = virtual_machines_list
        self.warm_migration = warm_migration
        self.target_namespace=target_namespace

    def to_dict(self):
        res = super().to_dict()
        res.update(
            {
                "spec": {
                    "warm" : self.warm_migration,
                    "targetNamespace" : self.target_namespace if self.target_namespace else self.namespace,
                    "map": {
                        "storage": {
                            "name": self.storage_map_name,
                            "namespace": self.storage_map_namespace,
                        },
                        "network": {
                            "name": self.storage_map_name,
                            "namespace": self.storage_map_namespace,
                        },
                    },
                    "vms": self.virtual_machines_list,
                    "provider": {
                        "source": {
                            "name": self.source_provider_name,
                            "namespace": self.source_provider_namespace,
                        },
                        "destination": {
                            "name": self.destination_provider_name,
                            "namespace": self.destination_provider_namespace,
                        },
                    },
                }
            }
        )
        return res

    def wait_for_condition_ready(self):
        self.wait_for_resource_status(
            condition_message=self.ConditionMessage.PLAN_READY,
            condition_status=self.Condition.Status.TRUE,
            condition_type=self.Condition.READY,
        )

    def wait_for_condition_successfully(self):
        self.wait_for_resource_status(
            condition_message=self.ConditionMessage.PLAN_SUCCEEDED,
            condition_status=self.Condition.Status.TRUE,
            condition_type=self.Status.SUCCEEDED
        )