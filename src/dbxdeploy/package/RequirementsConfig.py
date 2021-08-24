class RequirementsConfig:

    __slots__ = [
        "include_dev_dependencies_flag",
        "include_credentials_flag",
        "exclude_index_info_flag",
        "exclude_file_dependencies_flag",
        "redact_credentials_flag",
    ]

    def __init__(
        self,
        include_dev_dependencies=False,
        include_credentials=False,
        exclude_index_info=False,
        exclude_file_dependencies=False,
        redact_credentials=False,
    ):
        super(RequirementsConfig, self).__setattr__("include_dev_dependencies_flag", include_dev_dependencies)
        super(RequirementsConfig, self).__setattr__("include_credentials_flag", include_credentials)
        super(RequirementsConfig, self).__setattr__("exclude_index_info_flag", exclude_index_info)
        super(RequirementsConfig, self).__setattr__("exclude_file_dependencies_flag", exclude_file_dependencies)
        super(RequirementsConfig, self).__setattr__("redact_credentials_flag", redact_credentials)

    def __setattr__(self, name, value):
        raise AttributeError(f"{self.__class__} cannot be modified")

    def include_dev_dependencies(self) -> "RequirementsConfig":
        new_obj = self.__copy()
        super(RequirementsConfig, new_obj).__setattr__("include_dev_dependencies_flag", True)
        return new_obj

    def include_credentials(self) -> "RequirementsConfig":
        new_obj = self.__copy()
        super(RequirementsConfig, new_obj).__setattr__("include_credentials_flag", True)
        return new_obj

    def exclude_index_info(self) -> "RequirementsConfig":
        new_obj = self.__copy()
        super(RequirementsConfig, new_obj).__setattr__("exclude_index_info_flag", True)
        return new_obj

    def exclude_file_dependencies(self) -> "RequirementsConfig":
        new_obj = self.__copy()
        super(RequirementsConfig, new_obj).__setattr__("exclude_file_dependencies_flag", True)
        return new_obj

    def redact_credentials(self) -> "RequirementsConfig":
        new_obj = self.__copy()
        super(RequirementsConfig, new_obj).__setattr__("redact_credentials_flag", True)
        return new_obj

    @property
    def should_include_dev_dependencies(self):
        return self.__getattribute__("include_dev_dependencies_flag")

    @property
    def should_include_credentials(self):
        return self.__getattribute__("include_credentials_flag")

    @property
    def should_exclude_index_info(self):
        return self.__getattribute__("exclude_index_info_flag")

    @property
    def should_exclude_file_dependencies(self):
        return self.__getattribute__("exclude_file_dependencies_flag")

    @property
    def should_redact_credentials(self):
        return self.__getattribute__("redact_credentials_flag")

    def __copy(self) -> "RequirementsConfig":
        attributes = [self.__getattribute__(attr) for attr in self.__slots__]

        return RequirementsConfig(*attributes)
