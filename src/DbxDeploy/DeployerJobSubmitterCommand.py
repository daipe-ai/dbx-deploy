from logging import Logger
from DbxDeploy.ContainerInit import ContainerInit
from DbxDeploy.Git.CurrentBranchResolver import CurrentBranchResolver
import sys
from pathlib import Path
from DbxDeploy.DeployerJobSubmitter import DeployerJobSubmitter
from DbxDeploy.Notebook.ConverterResolver import ConverterResolver
import asyncio

class DeployerJobSubmitterCommand:

    @classmethod
    def run(cls):
        if len(sys.argv) < 2:
            raise Exception('dbx-deploy requires exactly 2 arguments [deploy YAML config path, notebook to run (relative path)]')

        deployYamlPath = Path(sys.argv[1])
        jupyterNotebookPath = Path(sys.argv[2])

        container = ContainerInit(CurrentBranchResolver()).init(deployYamlPath)

        converterResolver = container.get(ConverterResolver) # type: ConverterResolver
        logger = container.get('logging.Logger') # type: Logger

        if converterResolver.isSupported(jupyterNotebookPath) is False:
            formatsDescription = ', '.join(converterResolver.getSupportedFormatsDescriptions())
            logger.error('Only {} can be submitted as Databricks job'.format(formatsDescription))
            exit(1)

        notebookPath = jupyterNotebookPath.relative_to('src').with_suffix('')

        deployerJobSubmitter = container.get(DeployerJobSubmitter)  # type: DeployerJobSubmitter

        loop = asyncio.get_event_loop()
        loop.run_until_complete(deployerJobSubmitter.deployAndSubmitJob(notebookPath))
