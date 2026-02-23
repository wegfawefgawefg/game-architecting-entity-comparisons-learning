from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Stats:
    health: int
    defense: int
    armor: int


class Unit:
    def __init__(self, name: str, stats: Stats) -> None:
        self.name = name
        self.stats = stats

    def kind(self) -> str:
        raise NotImplementedError

    def special(self) -> None:
        print(f"{self.kind()} {self.name} has no special action.")

    def health(self) -> int:
        return self.stats.health

    def defense(self) -> int:
        return self.stats.defense

    def armor(self) -> int:
        return self.stats.armor

    def step(self) -> None:
        print(f"{self.kind()} {self.name} steps forward.")

    def take_damage(self, raw_damage: int) -> None:
        reduced = max(0, raw_damage - self.defense() - self.armor())
        self.stats.health = max(0, self.stats.health - reduced)
        print(
            f"{self.kind()} {self.name} takes {reduced} "
            f"(raw {raw_damage}), hp now {self.stats.health}"
        )

    def is_alive(self) -> bool:
        return self.health() > 0


class Bat(Unit):
    def __init__(self, name: str, stats: Stats, echolocation_level: int) -> None:
        super().__init__(name, stats)
        self.echolocation_level = echolocation_level

    def kind(self) -> str:
        return "Bat"

    def special(self) -> None:
        print(
            f"Bat {self.name} screeches with echolocation lvl {self.echolocation_level}"
        )


class Skeleton(Unit):
    def __init__(self, name: str, stats: Stats, bones: int) -> None:
        super().__init__(name, stats)
        self.bones = bones

    def kind(self) -> str:
        return "Skeleton"

    def special(self) -> None:
        print(f"Skeleton {self.name} rattles {self.bones} bones")


class Human(Unit):
    def __init__(self, name: str, stats: Stats, stamina: int) -> None:
        super().__init__(name, stats)
        self.stamina = stamina

    def kind(self) -> str:
        return "Human"

    def special(self) -> None:
        print(f"Human {self.name} adapts with stamina {self.stamina}")


def main() -> None:
    party: list[Unit] = [
        Bat("Flit", Stats(health=35, defense=1, armor=0), echolocation_level=7),
        Skeleton("Rattle", Stats(health=55, defense=2, armor=3), bones=206),
        Human("Ari", Stats(health=70, defense=4, armor=2), stamina=12),
    ]

    for unit in party:
        unit.step()
        unit.special()
        print(
            f"status -> hp: {unit.health()}, def: {unit.defense()}, armor: {unit.armor()}"
        )
        print()

    print("Incoming attack for 10 damage each:")
    for unit in party:
        unit.take_damage(10)

    print("\nAlive check:")
    for unit in party:
        alive = "true" if unit.is_alive() else "false"
        print(f"{unit.kind()} {unit.name} alive: {alive}")


if __name__ == "__main__":
    main()
