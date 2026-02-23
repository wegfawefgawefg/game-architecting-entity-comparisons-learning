#include <algorithm>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

struct Stats {
    int health;
    int defense;
    int armor;
};

class Unit {
public:
    Unit(std::string name, Stats stats) : name_(std::move(name)), stats_(stats) {}
    virtual ~Unit() = default;

    virtual const char* kind() const = 0;
    virtual void special() const {
        std::cout << kind() << " " << name_ << " has no special action.\n";
    }

    const std::string& name() const { return name_; }
    int health() const { return stats_.health; }
    int defense() const { return stats_.defense; }
    int armor() const { return stats_.armor; }

    void step() const {
        std::cout << kind() << " " << name_ << " steps forward.\n";
    }

    void takeDamage(int rawDamage) {
        const int reduced = std::max(0, rawDamage - defense() - armor());
        stats_.health = std::max(0, stats_.health - reduced);
        std::cout << kind() << " " << name_ << " takes " << reduced
                  << " (raw " << rawDamage << "), hp now " << stats_.health << "\n";
    }

    bool isAlive() const { return health() > 0; }

protected:
    std::string name_;
    Stats stats_;
};

class Bat final : public Unit {
public:
    Bat(std::string name, Stats stats, int echolocationLevel)
        : Unit(std::move(name), stats), echolocationLevel_(echolocationLevel) {}

    const char* kind() const override { return "Bat"; }

    void special() const override {
        std::cout << "Bat " << name_ << " screeches with echolocation lvl "
                  << echolocationLevel_ << "\n";
    }

private:
    int echolocationLevel_;
};

class Skeleton final : public Unit {
public:
    Skeleton(std::string name, Stats stats, int bones)
        : Unit(std::move(name), stats), bones_(bones) {}

    const char* kind() const override { return "Skeleton"; }

    void special() const override {
        std::cout << "Skeleton " << name_ << " rattles " << bones_ << " bones\n";
    }

private:
    int bones_;
};

class Human final : public Unit {
public:
    Human(std::string name, Stats stats, int stamina)
        : Unit(std::move(name), stats), stamina_(stamina) {}

    const char* kind() const override { return "Human"; }

    void special() const override {
        std::cout << "Human " << name_ << " adapts with stamina " << stamina_ << "\n";
    }

private:
    int stamina_;
};

int main() {
    std::vector<std::unique_ptr<Unit>> party;
    party.push_back(std::make_unique<Bat>("Flit", Stats{35, 1, 0}, 7));
    party.push_back(std::make_unique<Skeleton>("Rattle", Stats{55, 2, 3}, 206));
    party.push_back(std::make_unique<Human>("Ari", Stats{70, 4, 2}, 12));

    for (const auto& unit : party) {
        unit->step();
        unit->special();
        std::cout << "status -> hp: " << unit->health()
                  << ", def: " << unit->defense()
                  << ", armor: " << unit->armor() << "\n\n";
    }

    std::cout << "Incoming attack for 10 damage each:\n";
    for (auto& unit : party) {
        unit->takeDamage(10);
    }

    std::cout << "\nAlive check:\n";
    for (const auto& unit : party) {
        std::cout << unit->kind() << " " << unit->name()
                  << " alive: " << (unit->isAlive() ? "true" : "false") << "\n";
    }

    return 0;
}
