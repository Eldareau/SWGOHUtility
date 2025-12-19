class Unique:
    def __init__(self, name, handlers):
        self.name = name
        self.handlers = handlers  # {"event_name": callback}

    def register(self, owner, game):
        for event_name, callback in self.handlers.items():
            # wrap callback to inject owner automatically
            def wrapped_callback(callback=callback, **ctx):
                return callback(owner=owner, **ctx)
            game.listeners.append((event_name, wrapped_callback))

def the_chosen_one():

    def on_crit(owner, attacker, targets, **kw):
        # GAS crit an enemy
        if attacker is owner:
            if not targets.is_galactic_legend:
                print(f"{targets.name} increase cooldowns by 1 on all moves due to {owner.name}'s unique.")
                for move in targets.moves:
                    move.increase_cooldown(1)

    def on_crited(owner, targets, **kw):
        if targets is owner:
            owner.dispel_all_debuffs()
            print(f"{owner.name} dispelled all debuffs due to his unique.")

    def on_after_attacked(owner, attacker, allies, move, **kw):
        if attacker not in allies and attacker is not owner and not attacker.in_his_turn:
            move.critical_chance = 0
            print(f"{attacker.name}'s critical chance to 0 for this attack.")

    def on_before_attack(owner, attacker, targets, **kw):
        if attacker is owner:
            if targets.protection <= 0:
                targets.manipulate_max_health(-0.2)  # permanent stacking reduction
                print(f"{targets.name}'s max health reduced by 20% due to {owner.name}'s unique.")

    return Unique("The Chosen One", {
        "on_crit"           : on_crit,
        "on_crited"         : on_crited,
        "on_after_attacked" : on_after_attacked,
        "on_before_attack"  : on_before_attack,
    })

def hero_with_no_fear():

    def on_unique_start_of_battle(owner, unit, allies, **kw):
        if unit is owner:
            allies_501st_nb = len([ally for ally in allies if "501st" in ally.tags])
            owner.physical_armor     *= 1.25 * allies_501st_nb
            owner.special_resistance *= 1.25 * allies_501st_nb
            owner.max_protection      = round(owner.max_protection * 1.15 * allies_501st_nb)
            owner.protection          = owner.max_protection
            owner.tenacity           *= 1.25 * allies_501st_nb
            if allies_501st_nb == len(allies):
                owner.counter_chance = 100.0
                owner.special_critical_chance  += 0.5
                owner.physical_critical_chance += 0.5

    def on_death(owner, allies, **kw):
        allies_501st = [a for a in allies if "501st" in a.tags]
        dead_501st   = [a for a in allies_501st if a.dead]

        if dead_501st == allies:
            owner.cant_be_crit = True

        if dead_501st == allies_501st:
            owner.physical_armor     /= 1.25
            owner.special_resistance /= 1.25
            owner.tenacity           /= 1.25
            owner.max_protection     /= 1.15

    return Unique("Hero with no Fear", {
        "on_unique_start_of_battle" : on_unique_start_of_battle,
        "on_death"                  : on_death,
    })

