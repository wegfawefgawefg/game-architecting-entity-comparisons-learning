#[derive(Debug, Clone)]
struct Stats {
    health: i32,
    defense: i32,
    armor: i32,
}

#[derive(Debug, Clone)]
struct Core {
    name: String,
    stats: Stats,
}

trait Unit {
    // Per-type requirements
    fn kind(&self) -> &'static str;
    fn core(&self) -> &Core;
    fn core_mut(&mut self) -> &mut Core;

    // Shared/default behavior for all units
    fn name(&self) -> &str {
        &self.core().name
    }

    fn health(&self) -> i32 {
        self.core().stats.health
    }

    fn defense(&self) -> i32 {
        self.core().stats.defense
    }

    fn armor(&self) -> i32 {
        self.core().stats.armor
    }

    fn step(&self) {
        println!("{} {} steps forward.", self.kind(), self.name());
    }

    fn take_damage(&mut self, raw_damage: i32) {
        let reduced = (raw_damage - self.defense() - self.armor()).max(0);
        let kind = self.kind();
        let name = self.name().to_string();

        let c = self.core_mut();
        c.stats.health = (c.stats.health - reduced).max(0);

        println!(
            "{} {} takes {} (raw {}), hp now {}",
            kind,
            name,
            reduced,
            raw_damage,
            c.stats.health
        );
    }

    fn is_alive(&self) -> bool {
        self.health() > 0
    }

    fn special(&self) {
        println!("{} {} has no special action.", self.kind(), self.name());
    }
}

struct Bat {
    core: Core,
    echolocation_level: u8,
}

impl Unit for Bat {
    fn kind(&self) -> &'static str {
        "Bat"
    }

    fn core(&self) -> &Core {
        &self.core
    }

    fn core_mut(&mut self) -> &mut Core {
        &mut self.core
    }

    fn special(&self) {
        println!(
            "Bat {} screeches with echolocation lvl {}",
            self.name(),
            self.echolocation_level
        );
    }
}

struct Skeleton {
    core: Core,
    bones: u32,
}

impl Unit for Skeleton {
    fn kind(&self) -> &'static str {
        "Skeleton"
    }

    fn core(&self) -> &Core {
        &self.core
    }

    fn core_mut(&mut self) -> &mut Core {
        &mut self.core
    }

    fn special(&self) {
        println!("Skeleton {} rattles {} bones", self.name(), self.bones);
    }
}

struct Human {
    core: Core,
    stamina: u32,
}

impl Unit for Human {
    fn kind(&self) -> &'static str {
        "Human"
    }

    fn core(&self) -> &Core {
        &self.core
    }

    fn core_mut(&mut self) -> &mut Core {
        &mut self.core
    }

    fn special(&self) {
        println!("Human {} adapts with stamina {}", self.name(), self.stamina);
    }
}

fn main() {
    let mut party: Vec<Box<dyn Unit>> = vec![
        Box::new(Bat {
            core: Core {
                name: "Flit".to_string(),
                stats: Stats {
                    health: 35,
                    defense: 1,
                    armor: 0,
                },
            },
            echolocation_level: 7,
        }),
        Box::new(Skeleton {
            core: Core {
                name: "Rattle".to_string(),
                stats: Stats {
                    health: 55,
                    defense: 2,
                    armor: 3,
                },
            },
            bones: 206,
        }),
        Box::new(Human {
            core: Core {
                name: "Ari".to_string(),
                stats: Stats {
                    health: 70,
                    defense: 4,
                    armor: 2,
                },
            },
            stamina: 12,
        }),
    ];

    for unit in &party {
        unit.step();
        unit.special();
        println!(
            "status -> hp: {}, def: {}, armor: {}",
            unit.health(),
            unit.defense(),
            unit.armor()
        );
        println!();
    }

    println!("Incoming attack for 10 damage each:");
    for unit in &mut party {
        unit.take_damage(10);
    }

    println!("\nAlive check:");
    for unit in &party {
        println!("{} {} alive: {}", unit.kind(), unit.name(), unit.is_alive());
    }
}
