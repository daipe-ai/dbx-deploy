class BlackChecker:
    def __init__(self, black_enabled: bool):
        self.__black_enabled = black_enabled

    @property
    def is_black_enabled(self) -> bool:
        return self.__black_enabled

    @property
    def is_black_installed(self) -> bool:
        try:
            import black  # noqa

            return True

        except ImportError:
            return False
