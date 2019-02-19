from lib.backend import Clan
from lib.ui import ClanUI

clan_ui_resources_name = \
    {
        Clan.GOD: "god",
        Clan.QUN: "qun",
        Clan.SHU: "shu",
        Clan.WEI: "wei",
        Clan.WU: "wu",
    }

clan_ui_resources = \
    {
        Clan.GOD: ClanUI(
            './resources/cards/front/god-magatama.png',
            './resources/cards/front/god-skill.png',
            './resources/cards/front/god-skill-up.png',
            './resources/cards/front/god-skill-middle.png',
            './resources/cards/front/god-skill-down.png',
        ),
        Clan.QUN: ClanUI(
            './resources/cards/front/qun-magatama.png',
            './resources/cards/front/qun-skill.png',
            './resources/cards/front/qun-skill-up.png',
            './resources/cards/front/qun-skill-middle.png',
            './resources/cards/front/qun-skill-down.png',
        ),
        Clan.SHU: ClanUI(
            './resources/cards/front/shu-magatama.png',
            './resources/cards/front/shu-skill.png',
            './resources/cards/front/shu-skill-up.png',
            './resources/cards/front/shu-skill-middle.png',
            './resources/cards/front/shu-skill-down.png',
        ),
        Clan.WEI: ClanUI(
            './resources/cards/front/wei-magatama.png',
            './resources/cards/front/wei-skill.png',
            './resources/cards/front/wei-skill-up.png',
            './resources/cards/front/wei-skill-middle.png',
            './resources/cards/front/wei-skill-down.png',
        ),
        Clan.WU: ClanUI(
            './resources/cards/front/wu-magatama.png',
            './resources/cards/front/wu-skill.png',
            './resources/cards/front/wu-skill-up.png',
            './resources/cards/front/wu-skill-middle.png',
            './resources/cards/front/wu-skill-down.png',
        )
    }
