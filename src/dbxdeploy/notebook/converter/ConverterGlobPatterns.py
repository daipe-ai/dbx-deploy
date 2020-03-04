class ConverterGlobPatterns:

    def __init__(
        self,
        converterClass: str,
        globPatterns: list
    ):
        self.__converterClass = converterClass
        self.__globPatterns = globPatterns

    @property
    def converterClass(self):
        return self.__converterClass

    @property
    def globPatterns(self):
        return self.__globPatterns
