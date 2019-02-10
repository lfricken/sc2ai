import sc2
from sc2.constants import UnitTypeId as UnitType
from sc2.position import Point2
from sc2.unit import Unit

from sc2ai.utils.Investments import Investments


class DecisionTaker:
    """
    Given target investments, what do we actually do?

    For Instance: If we need to invest money in production, this class should tell a worker to build a Barracks.
    """

    bot: sc2.BotAI = None
    """Reference to our bot to grab game state data."""

    def __init__(self, bot: sc2.BotAI):
        self.bot = bot

    async def do_action(self, target_investments: Investments, current_investments: Investments) -> None:
        """TODO: this should actually remember the investments its made per loop so as to not overdo it"""

        invest_more_in = target_investments.minus(current_investments)

        if invest_more_in.army > 0:
            for rax in self.bot.units(UnitType.BARRACKS).ready.noqueue:
                if not self.bot.can_afford(UnitType.MARINE):
                    break
                await self.bot.do(rax.train(UnitType.MARINE))

        if invest_more_in.production > 0:
            depots = self.bot.units(UnitType.SUPPLYDEPOT) | self.bot.units(UnitType.SUPPLYDEPOTLOWERED)
            if depots.ready.exists:
                await self.try_make_another(UnitType.BARRACKS)

        if invest_more_in.expand > 0:
            await self.bot.expand_now()

        if invest_more_in.worker > 0:
            for _ in self.bot.units(UnitType.COMMANDCENTER).ready:
                town_hall: Unit = _
                if self.bot.can_afford(UnitType.SCV) and town_hall.noqueue:
                    await self.bot.do(town_hall.train(UnitType.SCV))

    async def try_make_another(self, unit_type: UnitType):
        if not self.bot.can_afford(unit_type):
            return
        if self.bot.already_pending(unit_type):
            # TODO: how do we handle this?
            return
        if self.bot.already_pending(unit_type) > 0:
            return

        workers = self.bot.workers.gathering  # grab a worker
        w = workers.random

        # determine position
        if self.bot.units(UnitType.BARRACKS):  # remaining rax go somewhere in base
            # TODO: we should find a way to just grab town hall in general, and not loop over all types of them
            town_hall: Unit = self.bot.units(UnitType.COMMANDCENTER).first
            ramp_center: Unit = self.bot.units(UnitType.BARRACKS).first

            center: Point2 = ramp_center.position + town_hall.position
            center = center / 2

            await self.bot.build(unit_type, near=center)

        else:  # first rax goes on ramp!
            position = self.bot.main_base_ramp.barracks_correct_placement
            await self.bot.do(w.build(unit_type, position))
