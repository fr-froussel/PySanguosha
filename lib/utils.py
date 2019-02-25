from lib.backend import Clan


class ClanUI:
    def __init__(self, main, main_lord, magatama, skill, skill_up, skill_middle, skill_down):
        """
        Construct clan UI resources association
        :param main: main image resource path
        :param main_lord: main lord image resource path
        :param magatama: life point resource path
        :param skill: skill name resource path
        :param skill_up: skill description resource path
        :param skill_middle: skill description resource path
        :param skill_down: skill description resource path
        """
        self.__main = main
        self.__main_lord = main_lord
        self.__magatama = magatama
        self.__skill = skill
        self.__skill_up = skill_up
        self.__skill_middle = skill_middle
        self.__skill_down = skill_down

    @property
    def main(self):
        return self.__main

    @property
    def main_lord(self):
        return self.__main_lord

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


clan_ui_resources = \
    {
        Clan.GOD: ClanUI(
            './resources/cards/front/god.png',
            './resources/cards/front/god.png',
            './resources/cards/front/god-magatama.png',
            './resources/cards/front/god-skill.png',
            './resources/cards/front/god-skill-up.png',
            './resources/cards/front/god-skill-middle.png',
            './resources/cards/front/god-skill-down.png',
        ),
        Clan.QUN: ClanUI(
            './resources/cards/front/qun.png',
            './resources/cards/front/qun-lord.png',
            './resources/cards/front/qun-magatama.png',
            './resources/cards/front/qun-skill.png',
            './resources/cards/front/qun-skill-up.png',
            './resources/cards/front/qun-skill-middle.png',
            './resources/cards/front/qun-skill-down.png',
        ),
        Clan.SHU: ClanUI(
            './resources/cards/front/shu.png',
            './resources/cards/front/shu-lord.png',
            './resources/cards/front/shu-magatama.png',
            './resources/cards/front/shu-skill.png',
            './resources/cards/front/shu-skill-up.png',
            './resources/cards/front/shu-skill-middle.png',
            './resources/cards/front/shu-skill-down.png',
        ),
        Clan.WEI: ClanUI(
            './resources/cards/front/wei.png',
            './resources/cards/front/wei-lord.png',
            './resources/cards/front/wei-magatama.png',
            './resources/cards/front/wei-skill.png',
            './resources/cards/front/wei-skill-up.png',
            './resources/cards/front/wei-skill-middle.png',
            './resources/cards/front/wei-skill-down.png',
        ),
        Clan.WU: ClanUI(
            './resources/cards/front/wu.png',
            './resources/cards/front/wu-lord.png',
            './resources/cards/front/wu-magatama.png',
            './resources/cards/front/wu-skill.png',
            './resources/cards/front/wu-skill-up.png',
            './resources/cards/front/wu-skill-middle.png',
            './resources/cards/front/wu-skill-down.png',
        )
    }


clan_ui_resources_name = \
    {
        Clan.GOD: "god",
        Clan.QUN: "qun",
        Clan.SHU: "shu",
        Clan.WEI: "wei",
        Clan.WU: "wu",
    }


spells_base_pos = [87, 375]

max_spells_size = (225, 215)
