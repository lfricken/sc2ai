from sc2reader.data import Unit

from utils.Investments import Investments


def unit_exists(unit: Unit, frame: int) -> bool:
    if unit.died_at is None:
        return unit.started_at <= frame
    else:
        if unit.started_at <= frame < unit.died_at:
            return True
        else:
            return False


def unit_started_during(unit: Unit, start_frame: int, end_frame: int) -> bool:
    if start_frame <= unit.started_at < end_frame:
        return True
    else:
        return False


def is_expand(unit: Unit) -> bool:
    if unit.title == "CommandCenter":
        return True
    if unit.title == "CommandCenterFlying":
        return True
    if unit.title == "OrbitalCommand":
        return True
    if unit.title == "OrbitalCommandFlying":
        return True
    if unit.title == "PlanetaryFortress":
        return True

    if unit.title == "Nexus":
        return True

    if unit.title == "Hatchery":
        return True
    if unit.title == "Lair":
        return True
    if unit.title == "Hive":
        return True


def is_production(unit: Unit) -> bool:
    if unit.title == "Barracks":
        return True
    if unit.title == "Factory":
        return True
    if unit.title == "Starport":
        return True
    if unit.title == "BarracksReactor":
        return True
    if unit.title == "FactoryReactor":
        return True
    if unit.title == "StarportReactor":
        return True

    if unit.title == "Gateway":
        return True
    if unit.title == "WarpGate":
        return True
    if unit.title == "RoboticsFacility":
        return True
    if unit.title == "Stargate":
        return True

    if unit.title == "SpawningPool":
        return True
    if unit.title == "RoachWarren":
        return True
    if unit.title == "BanelingNest":
        return True
    if unit.title == "HydraliskDen":
        return True
    if unit.title == "Spire":
        return True
    if unit.title == "InfestationPit":
        return True
    if unit.title == "UltraliskCavern":
        return True
    if unit.title == "GreaterSpire":
        return True


def get_time_delta(increment: int) -> int:
    """Use 5 second increments."""
    return 112 * increment  # 22.4 frames per second * 5seconds


def is_existing_army(unit: Unit, current_frame):
    if unit.name == "Overlord" or unit.name == "OverseerCocoon" or unit.name == "Overseer":
        return False
    else:
        return unit.is_army and unit_exists(unit, current_frame)


def is_existing_worker(unit: Unit, current_frame):
    return unit.is_worker and unit_exists(unit, current_frame)


def is_existing_expand(unit: Unit, current_frame):
    return is_expand(unit) and unit_exists(unit, current_frame)


def is_existing_production(unit: Unit, current_frame):
    return is_production(unit) and unit_exists(unit, current_frame)


def unit_value(unit: Unit):
    return unit.minerals + unit.vespene


class PlayerData:
    """
    Contains data about this player over the course of the game.
    Used for a neural network to train on successful investment strategies.
    """

    won_the_game: bool
    """True if this player won the game."""
    value_over_time = [Investments]
    """How much value at a given time."""
    total_frames: int = 0
    """How many frames were in the whole game."""

    def __init__(self, player, total_frames: int):
        self.total_frames = total_frames
        self.set_value_array(player)
        self.won_the_game = (player.result == "Win")

    def set_value_array(self, player):
        self.value_over_time: [Investments] = list()
        increment = 0
        current_frame = 0

        while current_frame < self.total_frames:
            self.value_over_time.append(Investments())
            self.process_units(player.units, current_frame)

            increment += 1
            current_frame = get_time_delta(increment)

    def process_units(self, units: [Unit], current_frame: int):
        for unit in units:
            if is_existing_army(unit, current_frame):
                self.value_over_time[-1].army += unit_value(unit)
            if is_existing_worker(unit, current_frame):
                self.value_over_time[-1].worker += unit_value(unit)
            if is_existing_expand(unit, current_frame):
                self.value_over_time[-1].expand += 400  # unit_value(unit)
            if is_existing_production(unit, current_frame):
                self.value_over_time[-1].production += unit_value(unit)
