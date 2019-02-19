class Clan:
    (
        GOD,
        QUN,
        SHU,
        WEI,
        WU
    ) = range(5)


class Character:
    def __init__(self, name, spells):
        """
        Character constructor
        :param name: name
        :param spells: spells list
        """
        self.__name = name
        self.__spells = spells

    @property
    def name(self):
        return self.__name

    @property
    def spells(self):
        return self.__spells


class Spell:
    def __init__(self, name, description):
        """
        Spell class constructor
        :param name: name spell
        :param description: description spell
        """
        self.__name = name
        self.__description = description

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description
