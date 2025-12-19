import debuffs
import buffs
import others

class Move :
    def __init__(self, name, max_cooldown, cooldown=0, defense_penetration=0, damage_multiplier=1, critical_chance=0, effects=None) :
        
        self.name = name
        self.max_cooldown = max_cooldown
        
        self.base_defense_penetration = defense_penetration
        self.base_damage_multiplier   = damage_multiplier
        self.base_critical_chance     = critical_chance
        self.base_cooldown            = cooldown
        self.base_ignore_defense      = False

        self.defense_penetration = self.base_defense_penetration
        self.damage_multiplier   = self.base_damage_multiplier
        self.critical_chance     = self.base_critical_chance
        self.cooldown            = self.base_cooldown
        self.ignore_defense      = self.base_ignore_defense

        self.effects = effects if effects is not None else []


    def __str__(self):
        return f"{self.name} ({self.cooldown})"
    
    def increase_cooldown(self, amount):
        self.cooldown = min(self.max_cooldown, self.cooldown + amount)

    def reset_temporary_modifiers(self):
        self.defense_penetration = self.base_defense_penetration
        self.damage_multiplier   = self.base_damage_multiplier
        self.critical_chance     = self.base_critical_chance
        self.cooldown            = self.base_cooldown
        self.ignore_defense      = self.base_ignore_defense

    def replace_moves_effect(self, unit, allies):
        #print(unit.name)
        moves = []
        match(self.before_effects["moves"]):
            case "self_basic":
                moves = {"unit":unit, "move":unit.moves[0]}
            case "self_moves":
                moves.extend({"unit":unit, "move":move} for move in unit.moves if move.base_cooldown != 0)
            case "allies_basic":
                moves.extend({"unit":ally, "move":ally.move[0]} for ally in allies)
            case "other_allies_basic":
                moves.extend({"unit":ally, "move":ally.move[0]} for ally in allies if ally is not unit)
        self.before_effects["moves"] = moves
        #print(moves)
        moves = []
        match(self.after_effects["moves"]):
            case "self_basic":
                moves = {"unit":unit, "move":unit.moves[0]}
            case "self_moves":
                moves.extend({"unit":unit, "move":move} for move in unit.moves if move.base_cooldown != 0)
            case "allies_basic":
                moves.extend({"unit":ally, "move":ally.move[0]} for ally in allies)
            case "other_allies_basic":
                moves.extend({"unit":ally, "move":ally.move[0]} for ally in allies if ally is not unit)
        self.after_effects["moves"] = moves
        #print(moves)

#General_Grievous
Furious_Assault   = Move("Furious Assault", 0,
                         effects=[{"phase":"before_hit", "scope":"per_cast", "type":"bonus", "targets":"self", "conditions":[{"targets":"enemy_target", "status":"debuffed"}], "bonus_damage_multiplier":0.3},
                                  {"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"enemy_target", "scaling":"self_max_health", "damage_base":0.2,"damage_variance":0.05, "cant_be":["evaded", "countered"]},
                                  {"phase":"after_hit", "scope":"per_target", "type":"debuff", "targets":"enemy_target", "kind":debuffs.Healing_Immunity.copy(duration=2)}])

Grievous_Wounds   = Move("Grievous Wounds", 4,
                         effects=[{"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"all_enemies", "scaling":"self_max_health", "damage_base":0.16,"damage_variance":0.05, "cant_be":["evaded"]},
                                  {"phase":"after_hit", "scope":"per_target", "type":"debuff", "targets":"all_enemies", "kind":debuffs.Target_Lock.copy(duration=2)},
                                  {"phase":"after_hit", "scope":"per_target", "type":"penalty", "targets":"all_enemies", "turn_meter_number":-0.3}])

Skittering_Horror = Move("Skittering Horror", 3,
                         effects=[{"phase":"before_hit", "scope":"per_cast", "type":"buff", "targets":"self", "kind":buffs.Health_Steal_Up.copy(duration=2)},
                                  {"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"enemy_target", "scaling":"self_max_health", "damage_base":0.3,"damage_variance":0.05, "cant_be":["evaded"]},
                                  {"phase":"after_hit", "scope":"per_cast", "type":"bonus", "targets":"self", "conditions":[{"targets":"enemy_target", "status":"debuffed"}], "max_health":0.1}, 
                                  {"phase":"after_hit", "scope":"per_cast", "type":"penalty", "targets":"enemy_target", "conditions":[{"targets":"enemy_target", "status":"debuffed"}], "max_health":-0.1, "cant_be":["resisted"]}, 
                                  {"phase":"after_hit", "scope":"per_target", "type":"debuff", "targets":"enemy_target", "kind":debuffs.Stun.copy(duration=1)}])

#General_Skywalker
Telekinesis      = Move("Telekinesis",  0,
                        effects=[{"phase":"before_hit", "scope":"per_cast", "type":"bonus", "targets":"self", "conditions":[{"targets":"enemy_target", "status":others.Armor_Shred}], "critical_hit":True},
                                 {"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"enemy_target", "scaling":"self_physical_damage", "damage_base":2.8,"damage_variance":0.05}, 
                                 {"phase":"after_hit", "scope":"per_cast", "type":"bonus", "targets":"self", "moves":[], "conditions":[{"targets":"enemy_target", "status":debuffs.Daze}], "turns_number":-1}])

Furious_Slash    = Move("Furious Slash", 0, defense_penetration=0.65,
                        effects=[{"phase":"before_hit", "scope":"per_cast", "type":"bonus", "targets":"self", "conditions":[{"targets":"all_allies", "tags":["501st"]}], "defense_penetration_multiplier":3},
                                 {"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"enemy_target", "scaling":"self_physical_damage", "damage_base":2.2,"damage_variance":0.05, "cant_be":["evaded"]}, 
                                 {"phase":"after_ability", "scope":"per_cast", "type":"call", "targets":"enemy_target", "moves":[Telekinesis], "conditions":[{"in_his_turn":True}]}])

Sundering_Strike = Move("Sundering Strike", 3,
                        effects=[{"phase":"before_hit", "scope":"per_cast", "type":"bonus", "targets":"self", "conditions":[{"targets":"enemy_target", "status":debuffs.Daze}], "bonus_damage_multiplier":2},
                                 {"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"enemy_target", "scaling":"self_physical_damage", "damage_base":3.5,"damage_variance":0.05},
                                 {"phase":"after_hit", "scope":"per_target", "type":"other", "targets":"enemy_target", "kind":others.Armor_Shred.copy(duration=-1)},
                                 {"phase":"after_ability", "scope":"per_cast", "type":"call", "targets":"enemy_target", "moves":[], "conditions":[{"has_used_ability_this_turn":False}]}])

Force_Grip       = Move("Force Grip", 3,
                        effects=[{"phase":"before_hit", "scope":"per_cast", "type":"bonus", "targets":"self", "conditions":[{"targets":"enemy_target", "status":others.Armor_Shred}], "critical_hit":True},
                                 {"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"all_enemies", "scaling":"self_physical_damage", "damage_base":3.0,"damage_variance":0.05},
                                 {"phase":"after_hit", "scope":"per_target", "type":"debuff", "targets":"all_enemies", "kind":debuffs.Daze.copy(duration=2)},
                                 {"phase":"after_ability", "scope":"per_cast", "type":"call", "targets":"enemy_target", "moves":[Sundering_Strike], "conditions":[{"has_used_ability_this_turn":False}]}])

Sundering_Strike.effects[3]["moves"] = [Force_Grip]
Telekinesis.effects[2]["moves"]      = [Sundering_Strike, Force_Grip]

#Jedi_Consular
Attack_As_Defense = Move("Attack As Defense", 3,
                         effects=[{"phase":"before_hit", "scope":"per_cast", "type":"bonus", "targets":"self", "conditions":[{"chance":0.5}], "ignore_defense":True},
                                  {"phase":"on_hit", "scope":"per_target", "type":"special", "targets":"enemy_target", "scaling":"self_special_damage", "damage_base":1.424,"damage_variance":0.05},
                                  {"phase":"after_hit", "scope":"per_target", "type":"healing", "targets":"self", "healing_from_damage_percent":0.3}])

Jedi_Healing      = Move("Jedi Healing", 5,
                         effects=[{"phase":"on_hit", "scope":"per_target", "type":"healing", "targets":"all_allies", "scaling":"self_max_health", "damage_base":0.4,"damage_variance":0},
                                  {"phase":"after_ability", "scope":"per_cast", "type":"bonus", "targets":"self", "conditions":[{"chance":0.5}], "turn_meter_number":0.25}])

Saber_Strike      = Move("Saber Strike", 0,
                         effects=[{"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"enemy_target", "scaling":"self_physical_damage", "damage_base":2.167,"damage_variance":0.05},
                                  {"phase":"after_hit", "scope":"per_cast", "type":"bonus", "targets":"self", "moves":[Jedi_Healing, Attack_As_Defense], "conditions":[{"chance":0.5}], "turns_number":-1}])