import numpy as np


def ignore(name: str):
    exceptions = ["INFESTEDTERRAN", "AUTOTURRET", "BROODLING", "LOCUST"]
    if any(bad in name for bad in exceptions):
        return True

    return False


def in_exceptions(name: str) -> bool:
    name = name.upper()
    exceptions = ["BURROWED", "FLYING", "UPROOTED", "COCOON", "ASSAULT", "BATTLE", "SIEGED", "LOWERED",
                  "CREEPTUMORQUEEN", "THORAP", "SIEGEMODE"]
    if any(bad in name for bad in exceptions):
        return True

    if ignore(name):
        return True

    return False


def fix_name(name: str) -> str:
    name = name.upper()

    if ignore(name):
        return ""

    # first replace
    if name == "CREEPTUMORQUEEN":
        return "CREEPTUMOR"

    if name == "THORAP":
        return "THOR"

    remove = ["BURROWED", "FLYING", "UPROOTED", "COCOON", "ASSAULT", "BATTLE", "SIEGED", "LOWERED", "SIEGEMODE"]
    for sub_str in remove:
        if sub_str in name:
            return name.replace(sub_str, "")

    return name


class Investments:
    investments: [int] = None

    def get_new(self) -> "Investments":
        return self.__class__()

    def __add__(self, other):
        """Add another investment to this one."""
        new_value = self.get_new()
        new_value.investments = np.add(self.investments, other.investments)
        return new_value

    def __sub__(self, other):
        """Subtract another investment to this one."""
        new_value = self.get_new()
        new_value.investments = np.subtract(self.investments, other.investments)
        return new_value

    def is_less_than_or_equal_to(self, other: "Investments") -> bool:
        temp = other - self
        return (temp.investments >= 0).all()

    def unit_was_built(self) -> bool:
        for i in self.investments:
            if i > 0:
                return True
        # no units were built
        return False
        
    def units_built(self) -> [int]:
        """Return array of units built"""
        units_built = self.get_new()
        for index, val in enumerate(self.investments):
            if i > 0:
                units_built[index] = self.investments[index]
        return units_built
        
    def copy(self):
        new_investments = self.get_new()
        new_investments.investments = np.copy(self.investments)
        return new_investments


class CoreInvestments(Investments):
    """
    How many resources, and invested in what?
    """

    @staticmethod
    def num_values() -> int:
        return 4

    investments: [int] = None

    def __init__(self):
        self.investments = np.full(CoreInvestments.num_values(), 0)

    @property
    def army(self) -> int:
        """Resources in military units."""
        return self.investments[0]

    @army.setter
    def army(self, value):
        self.investments[0] = value

    @property
    def production(self) -> int:
        """Resources in production potential."""
        return self.investments[1]

    @production.setter
    def production(self, value):
        self.investments[1] = value

    @property
    def worker(self) -> int:
        """Resources in worker units."""
        return self.investments[2]

    @worker.setter
    def worker(self, value):
        self.investments[2] = value

    @property
    def expand(self) -> int:
        """Resources in town centers."""
        return self.investments[3]

    @expand.setter
    def expand(self, value):
        self.investments[3] = value


class TerranInvestments(Investments):
    investments: np.ndarray = None

    @staticmethod
    def num_values() -> int:
        return 38

    def __init__(self):
        self.investments = np.full(TerranInvestments.num_values(), 0)

    @property
    def COMMANDCENTER(self) -> int:
        return self.investments[0]

    @COMMANDCENTER.setter
    def COMMANDCENTER(self, value):
        self.investments[0] = value

    @property
    def ORBITALCOMMAND(self) -> int:
        return self.investments[1]

    @ORBITALCOMMAND.setter
    def ORBITALCOMMAND(self, value):
        self.investments[1] = value

    @property
    def SCV(self) -> int:
        return self.investments[2]

    @SCV.setter
    def SCV(self, value):
        self.investments[2] = value

    @property
    def SUPPLYDEPOT(self) -> int:
        return self.investments[3]

    @SUPPLYDEPOT.setter
    def SUPPLYDEPOT(self, value):
        self.investments[3] = value

    @property
    def BARRACKS(self) -> int:
        return self.investments[4]

    @BARRACKS.setter
    def BARRACKS(self, value):
        self.investments[4] = value

    @property
    def REFINERY(self) -> int:
        return self.investments[5]

    @REFINERY.setter
    def REFINERY(self, value):
        self.investments[5] = value

    @property
    def MULE(self) -> int:
        return self.investments[6]

    @MULE.setter
    def MULE(self, value):
        self.investments[6] = value

    @property
    def REAPER(self) -> int:
        return self.investments[7]

    @REAPER.setter
    def REAPER(self, value):
        self.investments[7] = value

    @property
    def FACTORY(self) -> int:
        return self.investments[8]

    @FACTORY.setter
    def FACTORY(self, value):
        self.investments[8] = value

    @property
    def MARINE(self) -> int:
        return self.investments[9]

    @MARINE.setter
    def MARINE(self, value):
        self.investments[9] = value

    @property
    def BARRACKSREACTOR(self) -> int:
        return self.investments[10]

    @BARRACKSREACTOR.setter
    def BARRACKSREACTOR(self, value):
        self.investments[10] = value

    @property
    def REACTOR(self) -> int:
        return self.investments[11]

    @REACTOR.setter
    def REACTOR(self, value):
        self.investments[11] = value

    @property
    def FACTORYREACTOR(self) -> int:
        return self.investments[12]

    @FACTORYREACTOR.setter
    def FACTORYREACTOR(self, value):
        self.investments[12] = value

    @property
    def STARPORT(self) -> int:
        return self.investments[13]

    @STARPORT.setter
    def STARPORT(self, value):
        self.investments[13] = value

    @property
    def BARRACKSTECHLAB(self) -> int:
        return self.investments[14]

    @BARRACKSTECHLAB.setter
    def BARRACKSTECHLAB(self, value):
        self.investments[14] = value

    @property
    def TECHLAB(self) -> int:
        return self.investments[15]

    @TECHLAB.setter
    def TECHLAB(self, value):
        self.investments[15] = value

    @property
    def STARPORTTECHLAB(self) -> int:
        return self.investments[16]

    @STARPORTTECHLAB.setter
    def STARPORTTECHLAB(self, value):
        self.investments[16] = value

    @property
    def FACTORYTECHLAB(self) -> int:
        return self.investments[17]

    @FACTORYTECHLAB.setter
    def FACTORYTECHLAB(self, value):
        self.investments[17] = value

    @property
    def HELLION(self) -> int:
        return self.investments[18]

    @HELLION.setter
    def HELLION(self, value):
        self.investments[18] = value

    @property
    def BANSHEE(self) -> int:
        return self.investments[19]

    @BANSHEE.setter
    def BANSHEE(self, value):
        self.investments[19] = value

    @property
    def ARMORY(self) -> int:
        return self.investments[20]

    @ARMORY.setter
    def ARMORY(self, value):
        self.investments[20] = value

    @property
    def ENGINEERINGBAY(self) -> int:
        return self.investments[21]

    @ENGINEERINGBAY.setter
    def ENGINEERINGBAY(self, value):
        self.investments[21] = value

    @property
    def CYCLONE(self) -> int:
        return self.investments[22]

    @CYCLONE.setter
    def CYCLONE(self, value):
        self.investments[22] = value

    @property
    def RAVEN(self) -> int:
        return self.investments[23]

    @RAVEN.setter
    def RAVEN(self, value):
        self.investments[23] = value

    @property
    def STARPORTREACTOR(self) -> int:
        return self.investments[24]

    @STARPORTREACTOR.setter
    def STARPORTREACTOR(self, value):
        self.investments[24] = value

    @property
    def SIEGETANK(self) -> int:
        return self.investments[25]

    @SIEGETANK.setter
    def SIEGETANK(self, value):
        self.investments[25] = value

    @property
    def MISSILETURRET(self) -> int:
        return self.investments[26]

    @MISSILETURRET.setter
    def MISSILETURRET(self, value):
        self.investments[26] = value

    @property
    def MEDIVAC(self) -> int:
        return self.investments[27]

    @MEDIVAC.setter
    def MEDIVAC(self, value):
        self.investments[27] = value

    @property
    def VIKING(self) -> int:
        return self.investments[28]

    @VIKING.setter
    def VIKING(self, value):
        self.investments[28] = value

    @property
    def THOR(self) -> int:
        return self.investments[29]

    @THOR.setter
    def THOR(self, value):
        self.investments[29] = value

    @property
    def PLANETARYFORTRESS(self) -> int:
        return self.investments[30]

    @PLANETARYFORTRESS.setter
    def PLANETARYFORTRESS(self, value):
        self.investments[30] = value

    @property
    def SENSORTOWER(self) -> int:
        return self.investments[31]

    @SENSORTOWER.setter
    def SENSORTOWER(self, value):
        self.investments[31] = value

    @property
    def MARAUDER(self) -> int:
        return self.investments[32]

    @MARAUDER.setter
    def MARAUDER(self, value):
        self.investments[32] = value

    @property
    def WIDOWMINE(self) -> int:
        return self.investments[33]

    @WIDOWMINE.setter
    def WIDOWMINE(self, value):
        self.investments[33] = value

    @property
    def BUNKER(self) -> int:
        return self.investments[34]

    @BUNKER.setter
    def BUNKER(self, value):
        self.investments[34] = value

    @property
    def GHOSTACADEMY(self) -> int:
        return self.investments[35]

    @GHOSTACADEMY.setter
    def GHOSTACADEMY(self, value):
        self.investments[35] = value

    @property
    def GHOST(self) -> int:
        return self.investments[36]

    @GHOST.setter
    def GHOST(self, value):
        self.investments[36] = value

    @property
    def FUSIONCORE(self) -> int:
        return self.investments[37]

    @FUSIONCORE.setter
    def FUSIONCORE(self, value):
        self.investments[37] = value


class ZergInvestments(Investments):
    investments: [int] = None

    @staticmethod
    def num_values() -> int:
        return 34

    def __init__(self):
        self.investments = np.full(ZergInvestments.num_values(), 0)

    @property
    def HATCHERY(self) -> int:
        return self.investments[0]

    @HATCHERY.setter
    def HATCHERY(self, value):
        self.investments[0] = value

    @property
    def LAIR(self) -> int:
        return self.investments[1]

    @LAIR.setter
    def LAIR(self, value):
        self.investments[1] = value

    @property
    def DRONE(self) -> int:
        return self.investments[2]

    @DRONE.setter
    def DRONE(self, value):
        self.investments[2] = value

    @property
    def OVERLORD(self) -> int:
        return self.investments[3]

    @OVERLORD.setter
    def OVERLORD(self, value):
        self.investments[3] = value

    @property
    def EXTRACTOR(self) -> int:
        return self.investments[4]

    @EXTRACTOR.setter
    def EXTRACTOR(self, value):
        self.investments[4] = value

    @property
    def SPAWNINGPOOL(self) -> int:
        return self.investments[5]

    @SPAWNINGPOOL.setter
    def SPAWNINGPOOL(self, value):
        self.investments[5] = value

    @property
    def ZERGLING(self) -> int:
        return self.investments[6]

    @ZERGLING.setter
    def ZERGLING(self, value):
        self.investments[6] = value

    @property
    def QUEEN(self) -> int:
        return self.investments[7]

    @QUEEN.setter
    def QUEEN(self, value):
        self.investments[7] = value

    @property
    def CREEPTUMOR(self) -> int:
        return self.investments[8]

    @CREEPTUMOR.setter
    def CREEPTUMOR(self, value):
        self.investments[8] = value

    @property
    def ROACHWARREN(self) -> int:
        return self.investments[9]

    @ROACHWARREN.setter
    def ROACHWARREN(self, value):
        self.investments[9] = value

    @property
    def SPORECRAWLER(self) -> int:
        return self.investments[10]

    @SPORECRAWLER.setter
    def SPORECRAWLER(self, value):
        self.investments[10] = value

    @property
    def ROACH(self) -> int:
        return self.investments[11]

    @ROACH.setter
    def ROACH(self, value):
        self.investments[11] = value

    @property
    def RAVAGER(self) -> int:
        return self.investments[12]

    @RAVAGER.setter
    def RAVAGER(self, value):
        self.investments[12] = value

    @property
    def OVERSEER(self) -> int:
        return self.investments[13]

    @OVERSEER.setter
    def OVERSEER(self, value):
        self.investments[13] = value

    @property
    def EVOLUTIONCHAMBER(self) -> int:
        return self.investments[14]

    @EVOLUTIONCHAMBER.setter
    def EVOLUTIONCHAMBER(self, value):
        self.investments[14] = value

    @property
    def INFESTATIONPIT(self) -> int:
        return self.investments[15]

    @INFESTATIONPIT.setter
    def INFESTATIONPIT(self, value):
        self.investments[15] = value

    @property
    def SWARMHOST(self) -> int:
        return self.investments[16]

    @SWARMHOST.setter
    def SWARMHOST(self, value):
        self.investments[16] = value

    @property
    def BANELINGNEST(self) -> int:
        return self.investments[17]

    @BANELINGNEST.setter
    def BANELINGNEST(self, value):
        self.investments[17] = value

    @property
    def BANELING(self) -> int:
        return self.investments[18]

    @BANELING.setter
    def BANELING(self, value):
        self.investments[18] = value

    @property
    def HYDRALISKDEN(self) -> int:
        return self.investments[19]

    @HYDRALISKDEN.setter
    def HYDRALISKDEN(self, value):
        self.investments[19] = value

    @property
    def HYDRALISK(self) -> int:
        return self.investments[20]

    @HYDRALISK.setter
    def HYDRALISK(self, value):
        self.investments[20] = value

    @property
    def SPIRE(self) -> int:
        return self.investments[21]

    @SPIRE.setter
    def SPIRE(self, value):
        self.investments[21] = value

    @property
    def MUTALISK(self) -> int:
        return self.investments[22]

    @MUTALISK.setter
    def MUTALISK(self, value):
        self.investments[22] = value

    @property
    def HIVE(self) -> int:
        return self.investments[23]

    @HIVE.setter
    def HIVE(self, value):
        self.investments[23] = value

    @property
    def ULTRALISKCAVERN(self) -> int:
        return self.investments[24]

    @ULTRALISKCAVERN.setter
    def ULTRALISKCAVERN(self, value):
        self.investments[24] = value

    @property
    def VIPER(self) -> int:
        return self.investments[25]

    @VIPER.setter
    def VIPER(self, value):
        self.investments[25] = value

    @property
    def GREATERSPIRE(self) -> int:
        return self.investments[26]

    @GREATERSPIRE.setter
    def GREATERSPIRE(self, value):
        self.investments[26] = value

    @property
    def ULTRALISK(self) -> int:
        return self.investments[27]

    @ULTRALISK.setter
    def ULTRALISK(self, value):
        self.investments[27] = value

    @property
    def CORRUPTOR(self) -> int:
        return self.investments[28]

    @CORRUPTOR.setter
    def CORRUPTOR(self, value):
        self.investments[28] = value

    @property
    def BROODLORD(self) -> int:
        return self.investments[29]

    @BROODLORD.setter
    def BROODLORD(self, value):
        self.investments[29] = value

    @property
    def SPINECRAWLER(self) -> int:
        return self.investments[30]

    @SPINECRAWLER.setter
    def SPINECRAWLER(self, value):
        self.investments[30] = value

    @property
    def INFESTOR(self) -> int:
        return self.investments[31]

    @INFESTOR.setter
    def INFESTOR(self, value):
        self.investments[31] = value

    @property
    def NYDUSNETWORK(self) -> int:
        return self.investments[32]

    @NYDUSNETWORK.setter
    def NYDUSNETWORK(self, value):
        self.investments[32] = value

    @property
    def NYDUSWORM(self) -> int:
        return self.investments[33]

    @NYDUSWORM.setter
    def NYDUSWORM(self, value):
        self.investments[33] = value


class ProtossInvestments:
    investments: np.ndarray = None
