import sc2
from sc2 import Race
from sc2.player import Bot, Human

from cannon_rush import CannonRushBot


def main():
    sc2.run_game(sc2.maps.get("Abyssal Reef LE"), [
        Human(Race.Terran),
        Bot(Race.Zerg, CannonRushBot())
    ], realtime=True)

if __name__ == '__main__':
    main()
