# How `intermediate_bases.py` Works

This file demonstrates **layered inheritance** (intermediate base classes), similar to Source-style entity trees.

## Class stack (top to bottom)

`BaseEntity -> BaseAnimating -> BaseCombatCharacter -> AIBaseNPC -> NPCCombine`

Each layer adds a new capability. Concrete game types (like `NPCCombine`) inherit everything below.

## 1) Data helpers

- `Vec2` (`src/intermediate_bases.py:6`) is a simple position struct (`x`, `y`).

## 2) Root base: `BaseEntity`

- Defined at `src/intermediate_bases.py:12`.
- Owns universal fields: `name`, `pos`.
- Defines default hooks:
  - `kind()` returns type label.
  - `think()` is the generic update behavior.

This is the minimum “thing in the world.”

## 3) Intermediate base: `BaseAnimating`

- Defined at `src/intermediate_bases.py:24`.
- Inherits `BaseEntity`.
- Calls `super().__init__(name, pos)` to initialize inherited fields.
- Adds animation fields/behavior: `model`, `current_anim`, `set_anim()`, and a new `think()`.

Now any child class automatically has entity + animation behavior.

## 4) Intermediate base: `BaseCombatCharacter`

- Defined at `src/intermediate_bases.py:40`.
- Inherits `BaseAnimating`.
- Adds combat state (`health`, `armor`) and `take_damage()`.

Now descendants are both animating entities and combat-capable.

## 5) Intermediate base: `AIBaseNPC`

- Defined at `src/intermediate_bases.py:55`.
- Inherits `BaseCombatCharacter`.
- Adds AI data (`squad`, `goal`) and decision logic (`decide()`).
- Overrides `think()`:
  1. Decide goal.
  2. Choose animation.
  3. Call `super().think()` to reuse animation-level think.

This is an important pattern: override + delegate upward.

## 6) Concrete type: `NPCCombine`

- Defined at `src/intermediate_bases.py:81`.
- Inherits `AIBaseNPC` and hardcodes combine-specific defaults.
- Adds `weapon` and `special_attack()`.
- Its `think()` sets a specific goal (`engage`), does combine behavior, then calls `super().think()`.

So `NPCCombine` gets all previous layers for free and only adds delta behavior.

## Runtime behavior in `main()`

- `world` is typed as `list[BaseEntity]` (`src/intermediate_bases.py:106`), but stores mixed derived objects.
- Loop 1 (`ent.think()`): Python resolves the **actual runtime type** and calls that class's override (polymorphism).
- Loop 2 (`isinstance(ent, BaseCombatCharacter)`): only combat-capable objects receive damage.

## Why this pattern is useful

- You avoid one giant class with every field.
- You avoid large `if type == ...` branching everywhere.
- Shared behavior lives once at the right layer.
- Concrete game classes stay small and focused.

## Quick mental model

- Use base classes for reusable capability layers.
- Use derived classes for game-specific behavior.
- Use `super()` to extend behavior without rewriting parent logic.

## Source Engine Mapping (Why Separate Layers)

The class shape in `src/intermediate_bases.py` maps to classic Source-style layering:

- `BaseEntity` ~= `CBaseEntity`
- `BaseAnimating` ~= `CBaseAnimating`
- `BaseCombatCharacter` ~= `CBaseCombatCharacter`
- `AIBaseNPC` ~= `CAI_BaseNPC`
- `NPCCombine` ~= concrete NPC class such as Combine variants

Why keep them separate:

- Reuse: common behavior is implemented once at the correct layer.
- Scope: classes only carry systems they need (entity, animation, combat, AI).
- Polymorphism: one `list[BaseEntity]` can still run per-entity logic.

## Are There Non-Animating Entities?

Yes. Real Source projects include many entities that are not animated:

- triggers and volumes
- logic/controller entities
- utility point entities

In this file, `BaseEntity("trigger_once", Vec2(0, 0))` in `main()` is the same idea: world object with no animation or combat state.

## Memory and Allocation (Source-Style vs Data-Oriented)

Typical Source-style OOP entity systems do **not** store all full entity objects in one tightly packed contiguous array by concrete type.

Common pattern:

- objects are individually allocated (or managed in pools with pointer/handle access)
- engine keeps contiguous helper tables (entity indices, handles, lookup slots)
- gameplay code accesses entities through base pointers/handles

Tradeoff:

- OOP inheritance + polymorphism + flexibility
- less ideal cache locality than a pure ECS/SoA layout

## How Combat Characters Intersect Triggers (Source-Style)

Naive approach is nested loops between combat entities and triggers. Source-style engines usually do:

1. Broadphase/spatial partition returns nearby candidates.
2. Narrowphase checks precise overlap on that subset.
3. Engine emits touch callbacks based on overlap state changes.

This scales better than global pairwise checks every frame.

## What "Events" Usually Mean Here

For trigger overlap, Source-style behavior is typically callback methods (virtual dispatch), not primarily an enum list collected every frame.

Typical callbacks:

- `StartTouch(other)`: overlap begins
- `Touch(other)`: overlap continues
- `EndTouch(other)`: overlap ends

Why start + end both matter:

- `StartTouch`: one-time enter effects
- `Touch`: continuous effects while inside
- `EndTouch`: cleanup/reset on exit

So conceptually these are "events," but implementation is usually direct method calls from movement/collision processing when state changes.
