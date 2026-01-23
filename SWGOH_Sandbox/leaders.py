import others
import debuffs

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
            owner.complete_turn(game)
    
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

def daunting_presence():
    
    def on_leader_start_of_battle(owner, leader, allies, enemies, **kw):
        if leader is owner:
             for enemy in enemies:
                 enemy.physical_critical_avoidance -= 0.40
                 enemy.special_critical_avoidance  -= 0.40
                 enemy.physical_armor             *= 0.50
                 enemy.special_resistance         *= 0.50
             print(f"Enemies lost Defense and Crit Avoidance due to {owner.name}.")

    def on_gain_debuff(owner, targets, **kw):
        if targets.side != owner.side and targets.has_debuff(debuffs.Target_Lock):
             targets.cant_counter = True

    def on_lose_debuff(owner, targets, **kw):
        if targets.side != owner.side and not targets.has_debuff(debuffs.Target_Lock):
             targets.cant_counter = False

    def on_resist(owner, targets, attacker, **kw):
        if attacker.side == owner.side and "droid" in attacker.tags and "dark_side" in attacker.side:
             attacker.potency += 0.10
             print(f"{attacker.name} gains 10% Potency (Stacking) due to {owner.name}.")

    def on_damage_taken(owner, targets, attacker, damage, type, game, **kw):
        if targets.side != owner.side: 
            if targets.has_debuff(debuffs.Target_Lock):
                 tm_gain = 0.02
                 teams = owner.get_teams(game.defending_team, game.attacking_team)
                 allies = list(teams["allies"])
                 if owner not in allies:
                     allies.append(owner)
                 for ally in allies:
                     if "droid" in ally.tags or "separatist" in ally.tags:
                         mult = 2 if ally is owner else 1
                         ally.manipulate_turn_meter(tm_gain * mult)
                 print(f"Allies gained TM due to damaged Target Locked enemy (Leader: {owner.name}).")

            if "dark_side" in targets.side:
                targets.manipulate_turn_meter(-0.05)
                print(f"{targets.name} lost 5% TM due to {owner.name}.")
            if "light_side" in targets.side:
                targets.potency -= 0.02
                print(f"{targets.name} lost 2% Potency due to {owner.name}.")

    return Leader("Daunting Presence", {
        "on_leader_start_of_battle": on_leader_start_of_battle,
        "on_gain_debuff": on_gain_debuff,
        "on_lose_debuff": on_lose_debuff,
        "on_resist": on_resist,
        "on_damage_taken": on_damage_taken
    })

def jedi_protector():
    def on_leader_start_of_battle(owner, leader, allies, enemies, **kw):
        if leader is owner:
             # Apply to leader(owner) and allies
             team = allies + [owner]
             for unit in team:
                 unit.tenacity += 0.25
                 if "jedi" in unit.tags:
                     # Add 45 Flat Defense to Physical Armor
                     # Formula: flat = (pct * 637.5) / (1 - pct)
                     # pct = flat / (flat + 637.5)
                     
                     # Physical
                     current_pct = unit.physical_armor
                     if current_pct < 1.0:
                         flat = (current_pct * 637.5) / (1.0 - current_pct)
                         flat += 45
                         unit.physical_armor = flat / (flat + 637.5)
                     
                     # Special
                     current_pct = unit.special_resistance
                     if current_pct < 1.0:
                         flat = (current_pct * 637.5) / (1.0 - current_pct)
                         flat += 45
                         unit.special_resistance = flat / (flat + 637.5)
             
             print(f"Allies gained Tenacity and Defense due to {owner.name}.")

    return Leader("Jedi Protector", {
        "on_leader_start_of_battle": on_leader_start_of_battle
    })

def stalwart_jedi_defender():
    def on_leader_start_of_battle(owner, leader, allies, enemies, **kw):
        if leader is owner:
             # Apply to leader(owner) and allies
             team = allies + [owner]
             for unit in team:
                 if "jedi" in unit.tags:
                     # Add 60 Flat Defense to Physical Armor and Special Resistance
                     
                     # Physical
                     current_pct = unit.physical_armor
                     if current_pct < 1.0:
                         flat = (current_pct * 637.5) / (1.0 - current_pct)
                         flat += 60
                         unit.physical_armor = flat / (flat + 637.5)
                     
                     # Special
                     current_pct = unit.special_resistance
                     if current_pct < 1.0:
                         flat = (current_pct * 637.5) / (1.0 - current_pct)
                         flat += 60
                         unit.special_resistance = flat / (flat + 637.5)
             
             print(f"Jedi allies gained 60 Defense due to {owner.name}.")

    return Leader("Stalwart Jedi Defender", {
        "on_leader_start_of_battle": on_leader_start_of_battle
    })

def jedi_strategist():
    def on_leader_start_of_battle(owner, leader, allies, enemies, **kw):
        if leader is owner:
            # Apply to all allies: 30 Defense
            # Apply to Jedi allies: 35% Counter Chance, 25% Counter Damage
            team = allies + [owner]
            for unit in team:
                # 30 Defense for ALL allies
                # Physical
                current_pct = unit.physical_armor
                if current_pct < 1.0:
                    flat = (current_pct * 637.5) / (1.0 - current_pct)
                    flat += 30
                    unit.physical_armor = flat / (flat + 637.5)
                
                # Special
                current_pct = unit.special_resistance
                if current_pct < 1.0:
                    flat = (current_pct * 637.5) / (1.0 - current_pct)
                    flat += 30
                    unit.special_resistance = flat / (flat + 637.5)

                if "jedi" in unit.tags:
                     unit.counter_chance += 0.35
                     unit.counter_damage += 0.25
        
            print(f"Allies gained 30 Defense. Jedi allies gained 35% Counter Chance and 25% Counter Damage due to {owner.name}.")

    return Leader("Jedi Strategist", {
        "on_leader_start_of_battle": on_leader_start_of_battle
    })
