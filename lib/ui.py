from lib.backend import Character, Spell


class ClanUI:
    def __init__(self, magatama, skill, skill_up, skill_middle, skill_down):
        """
        Construct clan UI resources association
        :param magatama: life point resource path
        :param skill: skill name resource path
        :param skill_up: skill description resource path
        :param skill_middle: skill description resource path
        :param skill_down: skill description resource path
        """
        self.__magatama = magatama
        self.__skill = skill
        self.__skill_up = skill_up
        self.__skill_middle = skill_middle
        self.__skill_down = skill_down

    @property
    def magatama(self):
        return self.__magatama

    @property
    def skill(self):
        return self.__skill

    @property
    def skill_up(self):
        return self.__skill_up

    @property
    def skill_middle(self):
        return self.__skill_middle

    @property
    def skill_down(self):
        return self.__skill_down


class SpellUI:
    def __init__(self, name, description):
        """
        Spell class constructor
        :param name: name spell
        :param description: description spell
        """
        self.__spell = Spell(name, description)

    @property
    def spell(self):
        return self.__spell


class CharacterUI:
    def __init__(self, character, background):
        """
        CharacterUI constructor
        :param character: Character object
        :param background: Background associated
        """
        self.__character = character
        self.__background = background
        self.__spellsUIManager = SpellsUIManager(character.spells)


class SpellsUIManager:
    def __init__(self, spells):
        """
        Spells UI manager
        :param spells: spells list
        """
        self.__spells = spells

    @property
    def spells(self):
        return self.__spells

    def add_spell(self, spell):
        self.__spells.append(spell)