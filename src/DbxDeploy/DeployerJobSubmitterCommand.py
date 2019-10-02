from DbxDeploy.ContainerInit import ContainerInit
from DbxDeploy.Git.CurrentBranchResolver import CurrentBranchResolver
import sys
from pathlib import Path, PurePosixPath
from DbxDeploy.DeployerJobSubmitter import DeployerJobSubmitter
import asyncio

class DeployerJobSubmitterCommand:

    @classmethod
    def run(cls):
        if len(sys.argv) < 2:
            raise Exception('dbx-deploy requires exactly 2 arguments [deploy YAML config path, notebook to run (relative path)]')

        deployYamlPath = Path(sys.argv[1])
        jupyterNotebookPath = PurePosixPath(sys.argv[2])

        if jupyterNotebookPath.suffix != '.ipynb':
            raise Exception('Only Jupyter notebooks files (*.ipynb) can be submitted as Databricks job')

        notebookPath = jupyterNotebookPath.relative_to('src').with_suffix('')

        container = ContainerInit(CurrentBranchResolver()).init(deployYamlPath)

        deployerJobSubmitter = container.get(DeployerJobSubmitter)  # type: DeployerJobSubmitter

        loop = asyncio.get_event_loop()
        loop.run_until_complete(deployerJobSubmitter.deployAndSubmitJob(notebookPath))
