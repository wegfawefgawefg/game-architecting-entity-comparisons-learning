from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class Vec2:
    x: float
    y: float


@dataclass
class BaseData:
    name: str
    pos: Vec2


@dataclass
class AnimatingData:
    model: str
    current_anim: str = "idle"


@dataclass
class CombatData:
    health: int
    armor: int


@dataclass
class AIData:
    squad: str
    goal: str = "patrol"


@dataclass
class CombineData:
    weapon: str = "SMG"


@dataclass
class EntityRecord:
    ent_id: int
    kind: str
    base: BaseData
    anim: AnimatingData | None = None
    combat: CombatData | None = None
    ai: AIData | None = None
    combine: CombineData | None = None


# "Function pointer" style callbacks for each entity kind.
ThinkFn = Callable[["World", int], None]
DamageFn = Callable[["World", int, int], None]


@dataclass
class VTable:
    think: ThinkFn
    take_damage: DamageFn | None = None


@dataclass
class World:
    entities: dict[int, EntityRecord]
    vtables: dict[str, VTable]
    next_id: int = 1

    def spawn(
        self,
        *,
        kind: str,
        name: str,
        pos: Vec2,
        anim: AnimatingData | None = None,
        combat: CombatData | None = None,
        ai: AIData | None = None,
        combine: CombineData | None = None,
    ) -> int:
        ent_id = self.next_id
        self.next_id += 1
        self.entities[ent_id] = EntityRecord(
            ent_id=ent_id,
            kind=kind,
            base=BaseData(name=name, pos=pos),
            anim=anim,
            combat=combat,
            ai=ai,
            combine=combine,
        )
        return ent_id


def set_anim(ent: EntityRecord, anim: str) -> None:
    if ent.anim is not None:
        ent.anim.current_anim = anim


def think_base(world: World, ent_id: int) -> None:
    ent = world.entities[ent_id]
    print(f"[{ent.kind}] {ent.base.name} idles at ({ent.base.pos.x}, {ent.base.pos.y})")


def think_animating(world: World, ent_id: int) -> None:
    ent = world.entities[ent_id]
    if ent.anim is None:
        raise ValueError(f"{ent.kind} missing AnimatingData")
    print(f"[{ent.kind}] {ent.base.name} plays '{ent.anim.current_anim}' on {ent.anim.model}")


def take_damage_combat(world: World, ent_id: int, raw: int) -> None:
    ent = world.entities[ent_id]
    if ent.combat is None:
        raise ValueError(f"{ent.kind} missing CombatData")
    dmg = max(0, raw - ent.combat.armor)
    ent.combat.health = max(0, ent.combat.health - dmg)
    print(f"[{ent.kind}] {ent.base.name} took {dmg}, hp now {ent.combat.health}")


def think_ai_base_npc(world: World, ent_id: int) -> None:
    ent = world.entities[ent_id]
    if ent.ai is None:
        raise ValueError(f"{ent.kind} missing AIData")
    print(f"[{ent.kind}] {ent.base.name} ({ent.ai.squad}) decides goal: {ent.ai.goal}")
    set_anim(ent, "walk" if ent.ai.goal == "patrol" else "idle")
    think_animating(world, ent_id)


def think_npc_combine(world: World, ent_id: int) -> None:
    ent = world.entities[ent_id]
    if ent.ai is None or ent.combine is None:
        raise ValueError(f"{ent.kind} missing AIData or CombineData")
    ent.ai.goal = "engage"
    print(f"[{ent.kind}] {ent.base.name} suppresses with {ent.combine.weapon}")
    think_ai_base_npc(world, ent_id)


def build_world() -> World:
    world = World(entities={}, vtables={})

    world.vtables["BaseEntity"] = VTable(think=think_base)
    world.vtables["BaseAnimating"] = VTable(think=think_animating)
    world.vtables["BaseCombatCharacter"] = VTable(
        think=think_animating,
        take_damage=take_damage_combat,
    )
    world.vtables["AIBaseNPC"] = VTable(
        think=think_ai_base_npc,
        take_damage=take_damage_combat,
    )
    world.vtables["NPCCombine"] = VTable(
        think=think_npc_combine,
        take_damage=take_damage_combat,
    )

    world.spawn(kind="BaseEntity", name="trigger_once", pos=Vec2(0, 0))
    world.spawn(
        kind="BaseAnimating",
        name="prop_fan",
        pos=Vec2(4, 2),
        anim=AnimatingData(model="models/fan.mdl"),
    )
    world.spawn(
        kind="BaseCombatCharacter",
        name="citizen",
        pos=Vec2(8, 3),
        anim=AnimatingData(model="models/citizen.mdl"),
        combat=CombatData(health=40, armor=1),
    )
    world.spawn(
        kind="AIBaseNPC",
        name="metrocop",
        pos=Vec2(10, 8),
        anim=AnimatingData(model="models/police.mdl"),
        combat=CombatData(health=60, armor=3),
        ai=AIData(squad="CivilProtection"),
    )
    world.spawn(
        kind="NPCCombine",
        name="combine_elite",
        pos=Vec2(15, 6),
        anim=AnimatingData(model="models/combine_soldier.mdl"),
        combat=CombatData(health=80, armor=5),
        ai=AIData(squad="Overwatch"),
        combine=CombineData(weapon="SMG"),
    )

    return world


def main() -> None:
    world = build_world()

    print("== Generic think pass through entity IDs ==")
    for ent_id, ent in world.entities.items():
        world.vtables[ent.kind].think(world, ent_id)

    print("\n== Combat-only behavior where available ==")
    for ent_id, ent in world.entities.items():
        dmg_fn = world.vtables[ent.kind].take_damage
        if dmg_fn is not None:
            dmg_fn(world, ent_id, 12)


if __name__ == "__main__":
    main()
