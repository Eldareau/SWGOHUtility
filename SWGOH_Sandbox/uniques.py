
import others
import debuffs
import buffs

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

    def on_before_attacked(owner, attacker, allies, move, **kw):
        if attacker not in allies and attacker is not owner and not attacker.in_his_turn:
            move.critical_chance = 0
            print(f"{attacker.name}'s critical chance to 0 for this attack.")

    def on_before_attack(owner, attacker, targets, **kw):
        if attacker is owner:
            if targets.protection <= 0:
                targets.manipulate_max_health(-0.2)  # permanent stacking reduction
                print(f"{targets.name}'s max health reduced by 20% due to {owner.name}'s unique.")

    return Unique("The Chosen One", {
        "on_crit"            : on_crit,
        "on_crited"          : on_crited,
        "on_before_attacked" : on_before_attacked,
        "on_before_attack"   : on_before_attack,
    })

def hero_with_no_fear():

    def on_unique_start_of_battle(owner, unit, allies, **kw):
        if unit is owner:
            allies_501st_nb = len([ally for ally in allies if "501st" in ally.tags])
            owner.physical_armor     *= 1 + 0.25 * allies_501st_nb
            owner.special_resistance *= 1 + 0.25 * allies_501st_nb
            owner.max_protection      = round(owner.max_protection * (1 + 0.15 * allies_501st_nb))
            owner.protection          = owner.max_protection
            owner.tenacity           *= 1 + 0.25 * allies_501st_nb
            if allies_501st_nb == len(allies):
                owner.counter_chance = 100.0
                owner.special_critical_chance  += 0.5
                owner.physical_critical_chance += 0.5

    def on_turn_end(owner, allies, **kw):
        other_alive_allies = [a for a in allies if a is not owner and not a.dead]
        if len(other_alive_allies) == 0 and not owner.in_his_turn:
            owner.turn_meter += 350
            print(f"{owner.name} gains 35% Turn Meter due to his unique.")

    def on_death(owner, allies, **kw):
        allies_501st = [a for a in allies if "501st" in a.tags]
        dead_501st   = [a for a in allies_501st if a.dead]

        if dead_501st == allies:
            owner.cant_be_crit = True

        if dead_501st == allies_501st:
            owner.physical_armor     /= 1 + 0.25
            owner.special_resistance /= 1 + 0.25
            owner.tenacity           /= 1 + 0.25
            owner.max_protection     /= 1 + 0.15

    return Unique("Hero with no Fear", {
        "on_unique_start_of_battle" : on_unique_start_of_battle,
        "on_death"                  : on_death,
        "on_turn_end"               : on_turn_end,
    })

def metalloid_monstrosity():
    
    def on_turn_start(owner, targets, allies, game, **kw):
        # targets is the unit starting the turn.
        
        # 1. Start of Grievous' Turn (owner is targets)
        if targets is owner:
            droids = [u for u in allies if not u.dead and "droid" in u.tags and u is not owner]
            for droid in droids:
                damage_percent = 0.16 if "light_side" in droid.side else 0.08
                damage = int(owner.max_health * damage_percent)
                # Droid takes damage. Should invoke apply_damage logic? Or direct?
                # "take damage equal to..." usually implies non-evadable true damage or physical? 
                # "This damage cannot defeat characters." -> need to handle this.
                current_hp = droid.health
                dmg_applied = min(damage, current_hp - 1)
                if dmg_applied > 0:
                    droid.health -= dmg_applied
                    print(f"{droid.name} takes {dmg_applied} damage from {owner.name}.")
            
            # Gain stats
            if droids:
                count = len(droids)
                increase = 0.05 * count
                owner.manipulate_max_health(increase)
                owner.potency += increase # Potency is flat 0-1 range usually?
                print(f"{owner.name} gains {increase*100}% Max Health and Potency.")

        # 2. Start of EVERY Character's Turn
        if owner.health < owner.max_health and not owner.dead:
            owner.dispel_all_debuffs()
            droids = [u for u in allies if not u.dead and "droid" in u.tags and u is not owner]
            if droids:
                # Mark healthiest droid
                healthiest = max(droids, key=lambda u: u.health / u.max_health) # Percent or raw? "healthiest" usually means % or flat? SWGOH usually raw HP + Prot? Or just HP? Assuming HP/Prot % sum or just HP. Let's use Raw Health + Protection.
                healthiest = max(droids, key=lambda u: u.health + u.protection)
                healthiest.add_debuff(debuffs.Marked.copy(duration=1)) # "until end of turn" -> duration=1?
                print(f"{owner.name} forced {healthiest.name} to Taunt (Marked).")

    def on_death(owner, targets, allies, **kw):
        # whenever a Droid or Separatist ally is defeated
        if targets in allies and targets is not owner:
            if "droid" in targets.tags or "separatist" in targets.tags:
                owner.dispel_all_debuffs()
                for move in owner.moves:
                    move.cooldown = 0
                owner.turn_meter += 1000 # Bonus Turn
                print(f"{owner.name} resets cooldowns and gains Bonus Turn due to ally death.")

    return Unique("Metalloid Monstrosity", {
        "on_turn_start" : on_turn_start,
        "on_death"      : on_death,
    })


def superior_bladework():
    
    def on_unique_start_of_battle(owner, unit, **kw):
        if unit is owner:
            owner.counter_chance += 0.35
            # +20% Offense
            owner.physical_damage *= 1.20
            owner.special_damage  *= 1.20
            print(f"{owner.name} gains 35% Counter Chance and 20% Offense from Unique.")

    return Unique("Superior Bladework", {
        "on_unique_start_of_battle": on_unique_start_of_battle
    })

def anti_droid_specialist():
    
    def on_before_attack(owner, attacker, targets, **kw):
        if attacker is owner and ("droid" in targets.tags or "droid" in targets.tags): 
            owner.eeth_koth_bonus_applied = True
            owner.original_crit_chance = owner.physical_critical_chance 
            owner.original_crit_dmg = owner.critical_damage
            
            owner.physical_critical_chance += 0.35
            owner.special_critical_chance  += 0.35
            owner.critical_damage          += 0.20
            print(f"{owner.name} gains 35% Crit Chance and 20% Crit Damage vs Droid.")

    def on_after_attack(owner, attacker, targets, **kw):
        if attacker is owner and getattr(owner, 'eeth_koth_bonus_applied', False):
            owner.physical_critical_chance -= 0.35
            owner.special_critical_chance  -= 0.35
            owner.critical_damage          -= 0.20
            owner.eeth_koth_bonus_applied = False
            print(f"{owner.name} resets stats after attack.")

    return Unique("Anti-Droid Specialist", {
        "on_before_attack": on_before_attack,
        "on_after_attack" : on_after_attack
    })
