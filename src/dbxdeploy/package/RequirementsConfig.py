class RequirementsConfig:
    def __init__(
        self,
        include_dev_dependencies=False,
        include_credentials=False,
        exclude_index_info=False,
        exclude_file_dependencies=False,
        redact_credentials=False,
    ):
        self.__include_dev_dependencies = include_dev_dependencies
        self.__include_credentials = include_credentials
        self.__exclude_index_info = exclude_index_info
        self.__exclude_file_dependencies = exclude_file_dependencies
        self.__redact_credentials = redact_credentials

    def include_dev_dependencies(self):
        self.__include_dev_dependencies = True

    def include_credentials(self):
        self.__include_credentials = True

    def exclude_index_info(self):
        self.__exclude_index_info = True

    def exclude_file_dependencies(self):
        self.__exclude_file_dependencies = True

    def redact_credentials(self):
        self.__redact_credentials = True

    @property
    def should_include_dev_dependencies(self):
        return self.__include_dev_dependencies

    @property
    def should_include_credentials(self):
        return self.__include_credentials

    @property
    def should_exclude_index_info(self):
        return self.__exclude_index_info

    @property
    def should_exclude_file_dependencies(self):
        return self.__exclude_file_dependencies

    @property
    def should_redact_credentials(self):
        return self.__redact_credentials
