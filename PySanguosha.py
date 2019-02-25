from lib.backend import Clan, Character, Spell
from lib.ui import CharacterUI

import os
generation_dir = 'generation'
if not os.path.exists(generation_dir):
    os.makedirs(generation_dir)

cao_zhen = Character('Cao Zhen',
                     3,
                     {
                         Spell('Sī dí', 'Whenever Cao Zhen uses an escape or any other player uses an escape during Cao Zhen\'s turn, he puts the top card of the deck on his general card. At the beginning of any other players action phase, Cao Zhen can discard one of these cards to reduce the number of attacks that the current player can use by one.'),
                         Spell('Dìng pǐn', 'When Chen Qun damages another player, he can discard any card that is different that the one used to cause damage. The damaged player then does a judgment. If it is black, they draw X cards, where X is the amount of damage they received and this player cannot be targeted by Production again this turn. If the judgment is red, Chen Qun flips his general card.'),
                         Spell('Fǎ ēn', 'When any player flips their general card or goes into chains, Chen Qun can let that player draw one.'),
                     },
                     Clan.WEI,
                     False)
cao_zhen_ui = CharacterUI(cao_zhen, './resources/cards/skins/1803.jpg')

if cao_zhen_ui.additionals_ui_ready:
  cao_zhen_ui.generate_ui()