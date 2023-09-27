from typing import Optional

from pydantic import BaseModel, typing

from prowler.lib.logger import logger
from prowler.providers.aws.lib.service.service import AWSService
from prowler.providers.aws.services.vpc.vpc_client import vpc_client


################################ ECS
class Elasticache(AWSService):
    def __init__(self, audit_info):
        # Call AWSService's __init__
        super().__init__(__class__.__name__, audit_info)
        self.elasticache_instances = []
        self.__describe_cache_clusters__()
        self.__get_public_subnets__()

    def __describe_cache_clusters__(self):
        logger.info("ECS - Describing Cache Clusters...")
        try:
            cache_clusters = self.client.describe_cache_clusters()["CacheClusters"]
            for cache_cluster in cache_clusters:
                self.elasticache_instances.append(
                    ElastiCacheInstance(
                        cache_cluster_id=cache_cluster["CacheClusterId"],
                        arn=cache_cluster["ARN"],
                        cache_node_type=cache_cluster["CacheNodeType"],
                        engine=cache_cluster["Engine"],
                        engine_version=cache_cluster["EngineVersion"],
                        availability_zone=cache_cluster["PreferredAvailabilityZone"],
                        subnet_group=self.client.describe_cache_subnet_groups(
                            CacheSubnetGroupName=cache_cluster["CacheSubnetGroupName"]
                        )["CacheSubnetGroups"],
                    )
                )
        except Exception as error:
            logger.error(
                f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}]: {error}"
            )

    def __get_public_subnets__(self):
        for instance in self.elasticache_instances:
            public_subnets = []
            for subnets in instance.subnet_group:
                for subnet in subnets["Subnets"]:
                    if vpc_client.vpc_subnets[subnet["SubnetIdentifier"]].public:
                        public_subnets.append(
                            vpc_client.vpc_subnets[subnet["SubnetIdentifier"]].id
                        )
            instance.public_subnets = public_subnets


class ElastiCacheInstance(BaseModel):
    cache_cluster_id: str
    arn: str
    cache_node_type: str
    engine: str
    engine_version: str
    availability_zone: str
    subnet_group: typing.Any
    public_subnets: Optional[list] = []