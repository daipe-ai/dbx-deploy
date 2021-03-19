from dbxdeploy.package.PackageBuilder import PackageBuilder
from dbxdeploy.package.PackageMetadata import PackageMetadata
from pathlib import Path
from logging import Logger
from dbxdeploy.deploy.TargetPathsResolver import TargetPathsResolver
from dbxdeploy.deploy.LocalPathsResolver import LocalPathsResolver
from dbxdeploy.package.PackageUploaderInterface import PackageUploaderInterface


class PackageDeployer:
    def __init__(
        self,
        project_base_dir: Path,
        offline_install: bool,
        logger: Logger,
        package_uploader: PackageUploaderInterface,
        package_builder: PackageBuilder,
        target_paths_resolver: TargetPathsResolver,
        local_paths_resolver: LocalPathsResolver,
    ):
        self.__project_base_dir = project_base_dir
        self.__offline_install = offline_install
        self.__logger = logger
        self.__package_uploader = package_uploader
        self.__package_builder = package_builder
        self.__target_paths_resolver = target_paths_resolver
        self.__local_paths_resolver = local_paths_resolver

    def deploy(self, package_metadata: PackageMetadata):
        def whl_content_ready_callback():
            if self.__offline_install:
                for dependency in package_metadata.dependencies:
                    dependency_local_path = self.__local_paths_resolver.get_dependency_dist_path(dependency)
                    dependency_filename = self.__local_paths_resolver.get_dependency_filename_from_path(dependency_local_path)
                    dependency_deploy_path = self.__target_paths_resolver.get_dependency_upload_path_for_deploy(
                        package_metadata, dependency_filename
                    )

                    if not self.__package_uploader.exists(dependency_deploy_path):
                        self.__upload(dependency_local_path, dependency_deploy_path)
                    else:
                        self.__logger.debug(f"Package at {dependency_deploy_path} already exists. Skipping...")

            master_package_local_path = self.__local_paths_resolver.get_package_dist_path(package_metadata)
            master_package_deploy_path = self.__target_paths_resolver.get_package_upload_path_for_deploy(package_metadata)

            self.__upload(master_package_local_path, master_package_deploy_path)

        self.__invoke(package_metadata, whl_content_ready_callback)

    def release(self, package_metadata: PackageMetadata):
        def whl_content_ready_callback():
            if self.__offline_install:
                for dependency in package_metadata.dependencies:
                    dependency_local_path = self.__local_paths_resolver.get_dependency_dist_path(dependency)
                    dependency_filename = self.__local_paths_resolver.get_dependency_filename_from_path(dependency_local_path)
                    dependency_release_path = self.__target_paths_resolver.get_dependency_upload_path_for_release(
                        package_metadata, dependency_filename
                    )

                    self.__upload(dependency_local_path, dependency_release_path)

            master_package_local_path = self.__local_paths_resolver.get_package_dist_path(package_metadata)
            master_package_release_path = self.__target_paths_resolver.get_package_upload_path_for_release(package_metadata)

            self.__upload(master_package_local_path, master_package_release_path)

        self.__invoke(package_metadata, whl_content_ready_callback)

    def __invoke(self, package_metadata: PackageMetadata, whl_content_ready_callback: callable):
        self.__logger.info("Building master package (WHL)")

        self.__package_builder.build(self.__project_base_dir, package_metadata)

        whl_content_ready_callback()

        self.__logger.info("App package uploaded")

    def __upload(self, local_path: Path, target_path: str):
        self.__logger.info(f"Uploading WHL package to {target_path}")

        with local_path.open("rb") as file:
            self.__package_uploader.upload(file.read(), target_path, overwrite=True)
