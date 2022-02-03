class Storage:
    def __init__(self, *, string=""):
        self.__string = string

    def append(self, letter) -> None:
        self.__string += letter

    def get(self) -> str:
        return self.__string

    def void(self) -> None:
        self.__string = ""
