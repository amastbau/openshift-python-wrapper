from ocp_resources.mtv import MTV
from ocp_resources.resource import NamespacedResource


class NetworkMap(NamespacedResource, MTV):
    """
    Migration Toolkit For Virtualization (MTV) NetworkMap object.

    Args:
        source_provider_name (str): MTV Source Provider CR name.
        source_provider_namespace (str): MTV Source Provider CR namespace.
        destination_provider_name (str): MTV Destination Provider CR name.
        destination_provider_namespace (str): MTV Destination Provider CR namespace.
        mapping (dict): Storage Resources Mapping
            Exaple:
                [ { "destination" : { "type": "pod",
                    "source" : { "id": "network-13" }},

                  { "destination" : { "name": "nad_cr_name",
                                      "namespace": "nad_cr_namespace",
                                      "type": "multus"},                                      
                    "source" : { "name": "VM Netowrk" }},

                ]
    """


    def __init__(
        self,
        name,
        namespace,
        mapping=None,
        source_provider_name=None,
        source_provider_namespace=None,
        destination_provider_name=None,
        destination_provider_namespace=None,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.mapping = mapping
        self.source_provider_name = source_provider_name
        self.source_provider_namespace = source_provider_namespace
        self.destination_provider_name = destination_provider_name
        self.destination_provider_namespace = destination_provider_namespace

    def to_dict(self):
        res = super().to_dict()
        res.update(
            {
                "spec": {
                    "map": self.mapping,
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
            condition_message=self.ConditionMessage.NETWORK_MAP_READY,
            condition_status=self.StatusCondition.Status.TRUE,
            condition_type=self.StatusCondition.Type.READY,
        )
