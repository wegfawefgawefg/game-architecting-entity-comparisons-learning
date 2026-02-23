from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Vec2:
    x: float
    y: float


class BaseEntity:
    def __init__(self, name: str, pos: Vec2) -> None:
        self.name = name
        self.pos = pos

    def kind(self) -> str:
        return "BaseEntity"

    def think(self) -> None:
        print(f"[{self.kind()}] {self.name} idles at ({self.pos.x}, {self.pos.y})")


class BaseAnimating(BaseEntity):
    def __init__(self, name: str, pos: Vec2, model: str) -> None:
        super().__init__(name, pos)
        self.model = model
        self.current_anim = "idle"

    def kind(self) -> str:
        return "BaseAnimating"

    def set_anim(self, anim: str) -> None:
        self.current_anim = anim

    def think(self) -> None:
        print(f"[{self.kind()}] {self.name} plays '{self.current_anim}' on {self.model}")


class BaseCombatCharacter(BaseAnimating):
    def __init__(self, name: str, pos: Vec2, model: str, health: int, armor: int) -> None:
        super().__init__(name, pos, model)
        self.health = health
        self.armor = armor

    def kind(self) -> str:
        return "BaseCombatCharacter"

    def take_damage(self, raw: int) -> None:
        dmg = max(0, raw - self.armor)
        self.health = max(0, self.health - dmg)
        print(f"[{self.kind()}] {self.name} took {dmg}, hp now {self.health}")


class AIBaseNPC(BaseCombatCharacter):
    def __init__(
        self,
        name: str,
        pos: Vec2,
        model: str,
        health: int,
        armor: int,
        squad: str,
    ) -> None:
        super().__init__(name, pos, model, health, armor)
        self.squad = squad
        self.goal = "patrol"

    def kind(self) -> str:
        return "AIBaseNPC"

    def decide(self) -> None:
        print(f"[{self.kind()}] {self.name} ({self.squad}) decides goal: {self.goal}")

    def think(self) -> None:
        self.decide()
        self.set_anim("walk" if self.goal == "patrol" else "idle")
        super().think()


class NPCCombine(AIBaseNPC):
    def __init__(self, name: str, pos: Vec2) -> None:
        super().__init__(
            name=name,
            pos=pos,
            model="models/combine_soldier.mdl",
            health=80,
            armor=5,
            squad="Overwatch",
        )
        self.weapon = "SMG"

    def kind(self) -> str:
        return "NPCCombine"

    def special_attack(self) -> None:
        print(f"[{self.kind()}] {self.name} suppresses with {self.weapon}")

    def think(self) -> None:
        self.goal = "engage"
        self.special_attack()
        super().think()


def main() -> None:
    world: list[BaseEntity] = [
        BaseEntity("trigger_once", Vec2(0, 0)),
        BaseAnimating("prop_fan", Vec2(4, 2), "models/fan.mdl"),
        BaseCombatCharacter("citizen", Vec2(8, 3), "models/citizen.mdl", 40, 1),
        AIBaseNPC("metrocop", Vec2(10, 8), "models/police.mdl", 60, 3, "CivilProtection"),
        NPCCombine("combine_elite", Vec2(15, 6)),
    ]

    print("== Generic think pass through BaseEntity references ==")
    for ent in world:
        ent.think()

    print("\n== Combat-only behavior where available ==")
    for ent in world:
        if isinstance(ent, BaseCombatCharacter):
            ent.take_damage(12)


if __name__ == "__main__":
    main()
