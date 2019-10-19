# pylint: disable = invalid-name
from DbxDeploy.ContainerInit import ContainerInit
from DbxDeploy.Git.CurrentBranchResolver import CurrentBranchResolver
import sys
from pathlib import Path
from DbxDeploy.Job.JobsDeleter import JobsDeleter
from DbxDeploy.Cluster.ClusterRestarter import ClusterRestarter
from logging import Logger

class JobsDeleterCommand:

    @classmethod
    def run(cls):
        deployYamlPath = Path(sys.argv[1])

        container = ContainerInit(CurrentBranchResolver()).init(deployYamlPath)

        logger = container.get(Logger.__module__ + '.' + Logger.__name__) # type: Logger
        clusterRestarter = container.get(ClusterRestarter) # type ClusterRestarter
        jobsDeleter = container.get(JobsDeleter) # type: JobsDeleter

        logger.info('Jobs deletion started')
        clusterRestarter.restart()
        jobsDeleter.removeAll()
