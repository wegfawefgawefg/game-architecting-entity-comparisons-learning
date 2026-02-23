#[derive(Debug, Clone)]
struct Stats {
    health: i32,
    defense: i32,
    armor: i32,
}

trait Unit {
    // Minimal per-type requirements
    fn kind(&self) -> &'static str;
    fn name(&self) -> &str;
    fn stats(&self) -> &Stats;
    fn stats_mut(&mut self) -> &mut Stats;

    // Default behavior shared by all units
    fn health(&self) -> i32 {
        self.stats().health
    }

    fn defense(&self) -> i32 {
        self.stats().defense
    }

    fn armor(&self) -> i32 {
        self.stats().armor
    }

    fn step(&self) {
        println!("{} {} steps forward.", self.kind(), self.name());
    }

    fn take_damage(&mut self, raw_damage: i32) {
        let reduced = (raw_damage - self.defense() - self.armor()).max(0);
        let kind = self.kind();
        let name = self.name().to_string();
        let s = self.stats_mut();
        s.health = (s.health - reduced).max(0);
        println!(
            "{} {} takes {} (raw {}), hp now {}",
            kind,
            name,
            reduced,
            raw_damage,
            s.health
        );
    }

    fn is_alive(&self) -> bool {
        self.health() > 0
    }

    // Extension point for unique type behavior
    fn special(&self) {
        println!("{} {} has no special action.", self.kind(), self.name());
    }
}

struct Bat {
    name: String,
    stats: Stats,
    echolocation_level: u8,
}

struct Skeleton {
    name: String,
    stats: Stats,
    bones: u32,
}

struct Human {
    name: String,
    stats: Stats,
    stamina: u32,
}

macro_rules! impl_unit {
    ($type:ty, $kind:literal, $special:expr) => {
        impl Unit for $type {
            fn kind(&self) -> &'static str {
                $kind
            }

            fn name(&self) -> &str {
                &self.name
            }

            fn stats(&self) -> &Stats {
                &self.stats
            }

            fn stats_mut(&mut self) -> &mut Stats {
                &mut self.stats
            }

            fn special(&self) {
                ($special)(self);
            }
        }
    };
}

impl_unit!(Bat, "Bat", |s: &Bat| {
    println!(
        "Bat {} screeches with echolocation lvl {}",
        s.name, s.echolocation_level
    );
});

impl_unit!(Skeleton, "Skeleton", |s: &Skeleton| {
    println!("Skeleton {} rattles {} bones", s.name, s.bones);
});

impl_unit!(Human, "Human", |s: &Human| {
    println!("Human {} adapts with stamina {}", s.name, s.stamina);
});

fn main() {
    let mut party: Vec<Box<dyn Unit>> = vec![
        Box::new(Bat {
            name: "Flit".to_string(),
            stats: Stats {
                health: 35,
                defense: 1,
                armor: 0,
            },
            echolocation_level: 7,
        }),
        Box::new(Skeleton {
            name: "Rattle".to_string(),
            stats: Stats {
                health: 55,
                defense: 2,
                armor: 3,
            },
            bones: 206,
        }),
        Box::new(Human {
            name: "Ari".to_string(),
            stats: Stats {
                health: 70,
                defense: 4,
                armor: 2,
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
