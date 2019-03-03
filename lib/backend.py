class Clan:
    (
        GOD,
        QUN,
        SHU,
        WEI,
        WU
    ) = range(5)

clan_label_associations = {
  'god': Clan.GOD,
  'qun': Clan.QUN,
  'shu': Clan.SHU,
  'wei': Clan.WEI,
  'wu': Clan.WU,
}


class CharactersManager:
    def __init__(self):
        self.__characters = []

    @staticmethod
    def from_json(json):
      """
      create character from json data
      :param json: json data
      :return: instance of CharactersManager populated
      """
      this = CharactersManager()

      json_characters = '_CharactersManager__characters'

      this.__characters = []

      if json_characters in json:
        for character in json[json_characters]:
          status, character = Character.from_json(character)
          if status:
            this.__characters.append(character)
      else:
        print('Cannot found {} in the json'.format(json_characters))
        init = False

      return this

    @property
    def characters(self):
        return self.__characters


class Character:
    def __init__(self, name = None, life_points = None, spells = None, clan = None, lord = None, background = None):
        """
        Character constructor
        :param name: name
        :param life_points: number of life points
        :param spells: spells list
        :param clan: character clan
        :param lord: if the character is a lord
        :param background: character background
        """
        self.__name = name
        self.__life_points = life_points
        if spells:
          self.__spells = spells
        else:
          self.__spells = []
        self.__clan = clan
        self.__lord = lord
        self.__god = (clan == Clan.GOD)
        self.__background = background

    @staticmethod
    def from_json(json):
      """
      create character instance from json data
      :param json: json data
      :return: Character instance
      """
      status = False
      this = Character()

      json_background = '_Character__background'
      json_clan = '_Character__clan'
      json_life_points = '_Character__life_points'
      json_lord = '_Character__lord'
      json_name = '_Character__name'
      json_spells = '_Character__spells'

      if (json_background in json) and (json_clan in json) and (json_life_points in json) and \
        (json_lord in json) and (json_name in json) and (json_spells in json):

        clan = json[json_clan]
        if clan in clan_label_associations:
          this.__background = json[json_background]
          this.__clan = clan_label_associations.get(clan)
          this.__life_points = json[json_life_points]
          this.__lord = json[json_lord]
          this.__god = (this.clan == Clan.GOD)
          this.__name = json[json_name]
          this.__spells = []

          for spell in json[json_spells]:
            spell_status, spell = Spell.from_json(spell)
            if spell_status:
              this.__spells.append(spell)
            else:
              status = False

          status = True
        else:
          print('Unrecognized character clan value "{}".'.format(clan))
          this = None

      else:
        delim = ", "
        print('Cannot found all mandatories entries ({}) in the json for character description'.format(
          json_background + delim + json_clan + delim +
          json_life_points + delim + json_lord + delim +
          json_name + delim + json_spells
        ))

      return status, this

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

    @property
    def lord(self):
        return self.__lord

    @property
    def god(self):
        return self.__god

    @property
    def background(self):
        return self.__background


class Spell:
    def __init__(self, name = None, description = None):
        """
        Spell class constructor
        :param name: name spell
        :param description: description spell
        """
        self.__name = name
        self.__description = description

    @staticmethod
    def from_json(json):
      """
      create spell instance from json data
      :param json: json data
      :return: Spell instance
      """
      this = Spell()
      status = False

      json_description = '_Spell__description'
      json_name = '_Spell__name'

      if (json_description in json) and (json_name in json):
        this.__description = json[json_description]
        this.__name = json[json_name]

        status = True
      else:
        delim = ", "
        print('Cannot found all mandatories entries ({}) in the json for character spell description'.format(
          json_description + delim + json_name
        ))
        this = None

      return status, this

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description
