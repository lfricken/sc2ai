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
	"""
	How many resources, and invested in what?
	"""

	@staticmethod
	def investment_threshold():
		"""Amount of money we should have before deciding how to invest again."""
		return 200

	@staticmethod
	def investment_amount():
		"""Amount of money we should we consider investing each time."""
		return 400

	investments: np.ndarray = None

	def __init__(self):
		self.investments = np.full(4, 0)

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
		temp = other.minus(self)
		return (temp.investments >= 0).all()

	@property
	def size(self) -> int:
		"""How big is our investment array."""
		return len(self.investments[0])

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


class ZergInvestments(Investments):

	def get_new(self) -> "ZergInvestments":
		return self.__class__()

	def num_values(self) -> int:
		return 38

	def __init__(self):
		self.investments = np.full(self.num_values(), 0)

	@property
	def HATCHERY(self) -> int:
		return self.investments[4]

	@HATCHERY.setter
	def HATCHERY(self, value):
		self.investments[4] = value

	@property
	def LAIR(self) -> int:
		return self.investments[5]

	@LAIR.setter
	def LAIR(self, value):
		self.investments[5] = value

	@property
	def DRONE(self) -> int:
		return self.investments[6]

	@DRONE.setter
	def DRONE(self, value):
		self.investments[6] = value

	@property
	def OVERLORD(self) -> int:
		return self.investments[7]

	@OVERLORD.setter
	def OVERLORD(self, value):
		self.investments[7] = value

	@property
	def EXTRACTOR(self) -> int:
		return self.investments[8]

	@EXTRACTOR.setter
	def EXTRACTOR(self, value):
		self.investments[8] = value

	@property
	def SPAWNINGPOOL(self) -> int:
		return self.investments[9]

	@SPAWNINGPOOL.setter
	def SPAWNINGPOOL(self, value):
		self.investments[9] = value

	@property
	def ZERGLING(self) -> int:
		return self.investments[10]

	@ZERGLING.setter
	def ZERGLING(self, value):
		self.investments[10] = value

	@property
	def QUEEN(self) -> int:
		return self.investments[11]

	@QUEEN.setter
	def QUEEN(self, value):
		self.investments[11] = value

	@property
	def CREEPTUMOR(self) -> int:
		return self.investments[12]

	@CREEPTUMOR.setter
	def CREEPTUMOR(self, value):
		self.investments[12] = value

	@property
	def ROACHWARREN(self) -> int:
		return self.investments[13]

	@ROACHWARREN.setter
	def ROACHWARREN(self, value):
		self.investments[13] = value

	@property
	def SPORECRAWLER(self) -> int:
		return self.investments[14]

	@SPORECRAWLER.setter
	def SPORECRAWLER(self, value):
		self.investments[14] = value

	@property
	def ROACH(self) -> int:
		return self.investments[15]

	@ROACH.setter
	def ROACH(self, value):
		self.investments[15] = value

	@property
	def RAVAGER(self) -> int:
		return self.investments[16]

	@RAVAGER.setter
	def RAVAGER(self, value):
		self.investments[16] = value

	@property
	def OVERSEER(self) -> int:
		return self.investments[17]

	@OVERSEER.setter
	def OVERSEER(self, value):
		self.investments[17] = value

	@property
	def EVOLUTIONCHAMBER(self) -> int:
		return self.investments[18]

	@EVOLUTIONCHAMBER.setter
	def EVOLUTIONCHAMBER(self, value):
		self.investments[18] = value

	@property
	def INFESTATIONPIT(self) -> int:
		return self.investments[19]

	@INFESTATIONPIT.setter
	def INFESTATIONPIT(self, value):
		self.investments[19] = value

	@property
	def SWARMHOST(self) -> int:
		return self.investments[20]

	@SWARMHOST.setter
	def SWARMHOST(self, value):
		self.investments[20] = value

	@property
	def BANELINGNEST(self) -> int:
		return self.investments[21]

	@BANELINGNEST.setter
	def BANELINGNEST(self, value):
		self.investments[21] = value

	@property
	def BANELING(self) -> int:
		return self.investments[22]

	@BANELING.setter
	def BANELING(self, value):
		self.investments[22] = value

	@property
	def HYDRALISKDEN(self) -> int:
		return self.investments[23]

	@HYDRALISKDEN.setter
	def HYDRALISKDEN(self, value):
		self.investments[23] = value

	@property
	def HYDRALISK(self) -> int:
		return self.investments[24]

	@HYDRALISK.setter
	def HYDRALISK(self, value):
		self.investments[24] = value

	@property
	def SPIRE(self) -> int:
		return self.investments[25]

	@SPIRE.setter
	def SPIRE(self, value):
		self.investments[25] = value

	@property
	def MUTALISK(self) -> int:
		return self.investments[26]

	@MUTALISK.setter
	def MUTALISK(self, value):
		self.investments[26] = value

	@property
	def HIVE(self) -> int:
		return self.investments[27]

	@HIVE.setter
	def HIVE(self, value):
		self.investments[27] = value

	@property
	def ULTRALISKCAVERN(self) -> int:
		return self.investments[28]

	@ULTRALISKCAVERN.setter
	def ULTRALISKCAVERN(self, value):
		self.investments[28] = value

	@property
	def VIPER(self) -> int:
		return self.investments[29]

	@VIPER.setter
	def VIPER(self, value):
		self.investments[29] = value

	@property
	def GREATERSPIRE(self) -> int:
		return self.investments[30]

	@GREATERSPIRE.setter
	def GREATERSPIRE(self, value):
		self.investments[30] = value

	@property
	def ULTRALISK(self) -> int:
		return self.investments[31]

	@ULTRALISK.setter
	def ULTRALISK(self, value):
		self.investments[31] = value

	@property
	def CORRUPTOR(self) -> int:
		return self.investments[32]

	@CORRUPTOR.setter
	def CORRUPTOR(self, value):
		self.investments[32] = value

	@property
	def BROODLORD(self) -> int:
		return self.investments[33]

	@BROODLORD.setter
	def BROODLORD(self, value):
		self.investments[33] = value

	@property
	def SPINECRAWLER(self) -> int:
		return self.investments[34]

	@SPINECRAWLER.setter
	def SPINECRAWLER(self, value):
		self.investments[34] = value

	@property
	def INFESTOR(self) -> int:
		return self.investments[35]

	@INFESTOR.setter
	def INFESTOR(self, value):
		self.investments[35] = value

	@property
	def NYDUSNETWORK(self) -> int:
		return self.investments[36]

	@NYDUSNETWORK.setter
	def NYDUSNETWORK(self, value):
		self.investments[36] = value

	@property
	def NYDUSWORM(self) -> int:
		return self.investments[37]

	@NYDUSWORM.setter
	def NYDUSWORM(self, value):
		self.investments[37] = value


class TerranInvestments(Investments):

	def get_new(self) -> "TerranInvestments":
		return self.__class__()

	def num_values(self) -> int:
		return 42

	def __init__(self):
		self.investments = np.full(self.num_values(), 0)

	@property
	def COMMANDCENTER(self) -> int:
		return self.investments[4]

	@COMMANDCENTER.setter
	def COMMANDCENTER(self, value):
		self.investments[4] = value

	@property
	def ORBITALCOMMAND(self) -> int:
		return self.investments[5]

	@ORBITALCOMMAND.setter
	def ORBITALCOMMAND(self, value):
		self.investments[5] = value

	@property
	def SCV(self) -> int:
		return self.investments[6]

	@SCV.setter
	def SCV(self, value):
		self.investments[6] = value

	@property
	def SUPPLYDEPOT(self) -> int:
		return self.investments[7]

	@SUPPLYDEPOT.setter
	def SUPPLYDEPOT(self, value):
		self.investments[7] = value

	@property
	def BARRACKS(self) -> int:
		return self.investments[8]

	@BARRACKS.setter
	def BARRACKS(self, value):
		self.investments[8] = value

	@property
	def REFINERY(self) -> int:
		return self.investments[9]

	@REFINERY.setter
	def REFINERY(self, value):
		self.investments[9] = value

	@property
	def MULE(self) -> int:
		return self.investments[10]

	@MULE.setter
	def MULE(self, value):
		self.investments[10] = value

	@property
	def REAPER(self) -> int:
		return self.investments[11]

	@REAPER.setter
	def REAPER(self, value):
		self.investments[11] = value

	@property
	def FACTORY(self) -> int:
		return self.investments[12]

	@FACTORY.setter
	def FACTORY(self, value):
		self.investments[12] = value

	@property
	def MARINE(self) -> int:
		return self.investments[13]

	@MARINE.setter
	def MARINE(self, value):
		self.investments[13] = value

	@property
	def BARRACKSREACTOR(self) -> int:
		return self.investments[14]

	@BARRACKSREACTOR.setter
	def BARRACKSREACTOR(self, value):
		self.investments[14] = value

	@property
	def REACTOR(self) -> int:
		return self.investments[15]

	@REACTOR.setter
	def REACTOR(self, value):
		self.investments[15] = value

	@property
	def FACTORYREACTOR(self) -> int:
		return self.investments[16]

	@FACTORYREACTOR.setter
	def FACTORYREACTOR(self, value):
		self.investments[16] = value

	@property
	def STARPORT(self) -> int:
		return self.investments[17]

	@STARPORT.setter
	def STARPORT(self, value):
		self.investments[17] = value

	@property
	def BARRACKSTECHLAB(self) -> int:
		return self.investments[18]

	@BARRACKSTECHLAB.setter
	def BARRACKSTECHLAB(self, value):
		self.investments[18] = value

	@property
	def TECHLAB(self) -> int:
		return self.investments[19]

	@TECHLAB.setter
	def TECHLAB(self, value):
		self.investments[19] = value

	@property
	def STARPORTTECHLAB(self) -> int:
		return self.investments[20]

	@STARPORTTECHLAB.setter
	def STARPORTTECHLAB(self, value):
		self.investments[20] = value

	@property
	def FACTORYTECHLAB(self) -> int:
		return self.investments[21]

	@FACTORYTECHLAB.setter
	def FACTORYTECHLAB(self, value):
		self.investments[21] = value

	@property
	def HELLION(self) -> int:
		return self.investments[22]

	@HELLION.setter
	def HELLION(self, value):
		self.investments[22] = value

	@property
	def BANSHEE(self) -> int:
		return self.investments[23]

	@BANSHEE.setter
	def BANSHEE(self, value):
		self.investments[23] = value

	@property
	def ARMORY(self) -> int:
		return self.investments[24]

	@ARMORY.setter
	def ARMORY(self, value):
		self.investments[24] = value

	@property
	def ENGINEERINGBAY(self) -> int:
		return self.investments[25]

	@ENGINEERINGBAY.setter
	def ENGINEERINGBAY(self, value):
		self.investments[25] = value

	@property
	def CYCLONE(self) -> int:
		return self.investments[26]

	@CYCLONE.setter
	def CYCLONE(self, value):
		self.investments[26] = value

	@property
	def RAVEN(self) -> int:
		return self.investments[27]

	@RAVEN.setter
	def RAVEN(self, value):
		self.investments[27] = value

	@property
	def STARPORTREACTOR(self) -> int:
		return self.investments[28]

	@STARPORTREACTOR.setter
	def STARPORTREACTOR(self, value):
		self.investments[28] = value

	@property
	def SIEGETANK(self) -> int:
		return self.investments[29]

	@SIEGETANK.setter
	def SIEGETANK(self, value):
		self.investments[29] = value

	@property
	def MISSILETURRET(self) -> int:
		return self.investments[30]

	@MISSILETURRET.setter
	def MISSILETURRET(self, value):
		self.investments[30] = value

	@property
	def MEDIVAC(self) -> int:
		return self.investments[31]

	@MEDIVAC.setter
	def MEDIVAC(self, value):
		self.investments[31] = value

	@property
	def VIKING(self) -> int:
		return self.investments[32]

	@VIKING.setter
	def VIKING(self, value):
		self.investments[32] = value

	@property
	def THOR(self) -> int:
		return self.investments[33]

	@THOR.setter
	def THOR(self, value):
		self.investments[33] = value

	@property
	def PLANETARYFORTRESS(self) -> int:
		return self.investments[34]

	@PLANETARYFORTRESS.setter
	def PLANETARYFORTRESS(self, value):
		self.investments[34] = value

	@property
	def SENSORTOWER(self) -> int:
		return self.investments[35]

	@SENSORTOWER.setter
	def SENSORTOWER(self, value):
		self.investments[35] = value

	@property
	def MARAUDER(self) -> int:
		return self.investments[36]

	@MARAUDER.setter
	def MARAUDER(self, value):
		self.investments[36] = value

	@property
	def WIDOWMINE(self) -> int:
		return self.investments[37]

	@WIDOWMINE.setter
	def WIDOWMINE(self, value):
		self.investments[37] = value

	@property
	def BUNKER(self) -> int:
		return self.investments[38]

	@BUNKER.setter
	def BUNKER(self, value):
		self.investments[38] = value

	@property
	def GHOSTACADEMY(self) -> int:
		return self.investments[39]

	@GHOSTACADEMY.setter
	def GHOSTACADEMY(self, value):
		self.investments[39] = value

	@property
	def GHOST(self) -> int:
		return self.investments[40]

	@GHOST.setter
	def GHOST(self, value):
		self.investments[40] = value

	@property
	def FUSIONCORE(self) -> int:
		return self.investments[41]

	@FUSIONCORE.setter
	def FUSIONCORE(self, value):
		self.investments[41] = value


class ProtossInvestments(Investments):
	def hi(self):
		return
