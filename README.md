# Game Architecting: Entity Comparisons (Learning)

Small learning repo for experimenting with game-entity architecture patterns across styles and languages.

## What this repo is for

- Compare OOP/inheritance entity design vs C-style IDs + data + function dispatch.
- Keep simple, runnable examples for discussion and iteration.
- Treat this as a scratchpad for architecture thinking, not production code.

## Current examples

- `src/intermediate_bases.py`: layered inheritance chain inspired by Source-style entity capability stacks.
- `src/intermediate_bases_cstyle.py`: C-style version using entity IDs, plain data records, and explicit behavior tables.
- `docs/intermediate_bases.md`: notes on tradeoffs, memory layout intuition, and trigger/touch event flow.
- `src/main.rs`, `src/nonmacro.rs`, `src/main.cpp`, `src/main.py`: additional playground files.

## Notes on quality expectations

This repo is intentionally exploratory. Examples may be incomplete or non-compiling depending on what is being tested that day.

## Date marker

Oldest preserved file timestamp in this repo: **January 17, 2025** (from `Cargo.toml` and `Cargo.lock`).

## License

See `LICENSE`.
