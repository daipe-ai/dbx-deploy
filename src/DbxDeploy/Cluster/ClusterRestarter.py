from databricks_api import DatabricksAPI
from logging import Logger

class ClusterRestarter:

    def __init__(
        self,
        clusterId: str,
        logger: Logger,
        dbxApi: DatabricksAPI
    ):
        self.__clusterId = clusterId
        self.__logger = logger
        self.__dbxApi = dbxApi

    def restart(self):
        self.__logger.info('Checking state of cluster {}'.format(self.__clusterId))
        cluster = self.__dbxApi.cluster.get_cluster(self.__clusterId)

        if cluster['state'] != 'PENDING' and cluster['state'] != 'RUNNING':
            self.__logger.info('Cannot in {} state, restart not needed'.format(cluster['state']))
            return

        self.__logger.info('Restarting cluster {}'.format(self.__clusterId))
        self.__dbxApi.cluster.restart_cluster(self.__clusterId)
