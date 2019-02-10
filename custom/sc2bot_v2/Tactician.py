import sc2

from sc2.constants import UnitTypeId as UnitType
from sc2.helpers import ControlGroup


class Tactician:
    """
    The purpose of the tactician is to make direct military
    decisions such as attack here, defend there, build turret here.
    """

    bot: sc2.BotAI = None
    attack_groups: [] = None
    """Reference to our bot to grab game state data."""

    def __init__(self, bot: sc2.BotAI):
        self.bot = bot
        self.attack_groups = set()

    async def update(self):

        if self.bot.units(UnitType.MARINE).idle.amount > 30:
            cg = ControlGroup(self.bot.units(UnitType.MARINE).idle)
            self.attack_groups.add(cg)

        for ac in list(self.attack_groups):
            alive_units = ac.select_units(self.bot.units)
            if alive_units.exists and alive_units.idle.exists:
                target = self.bot.known_enemy_structures.random_or(self.bot.enemy_start_locations[0]).position
                for marine in ac.select_units(self.bot.units):
                    await self.bot.do(marine.attack(target))
            else:
                self.attack_groups.remove(ac)
