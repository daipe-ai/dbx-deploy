from dbxdeploy.utils.DatabricksClient import DatabricksClient
from logging import Logger


class ClusterRestarter:
    def __init__(self, logger: Logger, dbx_api: DatabricksClient):
        self.__logger = logger
        self.__dbx_api = dbx_api

    def restart(self, cluster_id: str):
        self.__logger.info("Checking state of cluster {}".format(cluster_id))
        cluster = self.__dbx_api.cluster.get_cluster(cluster_id)

        if cluster["state"] != "PENDING" and cluster["state"] != "RUNNING":
            self.__logger.info("Cannot in {} state, restart not needed".format(cluster["state"]))
            return

        self.__logger.info("Restarting cluster {}".format(cluster_id))
        self.__dbx_api.cluster.restart_cluster(cluster_id)
