from databricks_api import DatabricksAPI
from logging import Logger


class ClusterRestarter:
    def __init__(self, cluster_id: str, logger: Logger, dbx_api: DatabricksAPI):
        self.__cluster_id = cluster_id
        self.__logger = logger
        self.__dbx_api = dbx_api

    def restart(self):
        self.__logger.info("Checking state of cluster {}".format(self.__cluster_id))
        cluster = self.__dbx_api.cluster.get_cluster(self.__cluster_id)

        if cluster["state"] != "PENDING" and cluster["state"] != "RUNNING":
            self.__logger.info("Cannot in {} state, restart not needed".format(cluster["state"]))
            return

        self.__logger.info("Restarting cluster {}".format(self.__cluster_id))
        self.__dbx_api.cluster.restart_cluster(self.__cluster_id)
