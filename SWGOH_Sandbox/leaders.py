import others

class Leader:
    def __init__(self, name, handlers):
        self.name = name
        self.handlers = handlers

    def register(self, owner, game):
        for event_name, callback in self.handlers.items():
            # wrap callback to inject owner automatically
            def wrapped_callback(callback=callback, **ctx):
                return callback(owner=owner, **ctx)
            game.listeners.append((event_name, wrapped_callback))

def general_of_the_501st():

    def on_leader_start_of_battle(owner, leader, allies, enemies, **kw):
        if leader is owner:
            owner.is_revivable = False
            owner.critical_damage *= 1.5
            owner.hp_lock = True
            for ally in allies :
                ally.is_revivable = False
                if len([ally for ally in allies if not ally.dead and "501st" in ally.tags]) >= 1:
                    owner.add_other(others.Advance.copy(duration=-1))
                    if "501st" in ally.tags:
                        ally.critical_damage *= 1.5
            for enemy in enemies:
                enemy.is_revivable = False
            print(f"All 501st allies gain 50% critical damage and no unit can be revived due to {owner.name}'s leader ability.")

    def on_turn_start(owner, targets, allies, **kw):
        if targets is owner and owner.has_other(others.Cover) and len([ally for ally in allies if not ally.dead and "501st" in ally.tags])>=1:
            owner.remove_other(others.Cover)
            owner.add_other(others.Advance.copy(duration=-1))
            owner.speed = owner.base_speed
            print(f"{owner.name} removes cover and resets speed at the start of his turn due to his leader ability.")

    def on_turn_end(owner, targets, **kw):
        multiplicator = 1
        if owner.has_other(others.Cover):
            if "501st" in targets.tags :
                multiplicator = 2
            owner.protection += owner.max_protection * 0.1 * multiplicator
            owner.turn_meter += 100 * multiplicator
            print(f"{owner.name} gains protection and turn meter when in cover at the end of anybody's turn due to his leader ability.")

    def on_death(owner, game, targets, allies, **kw):
        if targets is not owner and targets in allies and len([ally for ally in allies if not ally.dead and "501st" in ally.tags])==0:
            owner.hp_lock = False
            owner.remove_other(others.Cover)
            owner.remove_other(others.Advance)
            owner.speed = owner.base_speed
            owner.complete_turn(owner, game)
    
    def on_after_attacked(owner, targets, allies, **kw):
        if targets is owner and owner.protection == 0 and len([ally for ally in allies if not ally.dead and "501st" in ally.tags])>=1:
            for ally in allies:
                ally.hp_lock = False
            owner.remove_everything()
            owner.add_other(others.Cover.copy(duration=-1))
            owner.turn_meter = 0
            owner.speed = 0
            print(f"{owner.name} is protected from being defeated due to his leader ability.")

    def on_gain_buff(owner, targets, enemies, allies, **kw):
        if targets in enemies:
            for ally in [ally for ally in allies if "501st" in ally.tags] :
                ally.manipulate_offense_stacking(0.02)
            owner.manipulate_offense_stacking(0.02)
            print(f"All 501st allies gain 2% offense when an enemy gains a buff due to {owner.name}'s leader ability.")

    return Leader("General of the 501st", {
        "on_leader_start_of_battle" : on_leader_start_of_battle,
        "on_turn_start"             : on_turn_start,
        "on_turn_end"               : on_turn_end,
        "on_death"                  : on_death,
        "on_after_attacked"         : on_after_attacked,
        "on_gain_buff"              : on_gain_buff
    })

