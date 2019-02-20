class Clan:
    (
        GOD,
        QUN,
        SHU,
        WEI,
        WU
    ) = range(5)


class Character:
    def __init__(self, name, life_points, spells, clan):
        """
        Character constructor
        :param name: name
        :param life_points: number of life points
        :param spells: spells list
        :param clan: character clan
        """
        self.__name = name
        self.__life_points = life_points
        self.__spells = spells
        self.__clan = clan

    @property
    def name(self):
        return self.__name

    @property
    def life_points(self):
        return self.__life_points

    @property
    def spells(self):
        return self.__spells

    @property
    def clan(self):
        return self.__clan


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
