import debuffs
import buffs
import others

class Move :
    def __init__(self, name, max_cooldown, cooldown=0, defense_penetration=0, damage_multiplier=1, critical_chance=0, ignore_defense=False, effects=None) :
        
        self.name = name
        self.max_cooldown = max_cooldown
        
        self.base_defense_penetration = defense_penetration
        self.base_damage_multiplier   = damage_multiplier
        self.base_critical_chance     = critical_chance
        self.base_cooldown            = cooldown
        self.base_ignore_defense      = ignore_defense

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
                moves.extend({"unit":ally, "move":ally.moves[0]} for ally in allies)
            case "other_allies_basic":
                moves.extend({"unit":ally, "move":ally.moves[0]} for ally in allies if ally is not unit)
        self.before_effects["moves"] = moves
        #print(moves)
        moves = []
        match(self.after_effects["moves"]):
            case "self_basic":
                moves = {"unit":unit, "move":unit.moves[0]}
            case "self_moves":
                moves.extend({"unit":unit, "move":move} for move in unit.moves if move.base_cooldown != 0)
            case "allies_basic":
                moves.extend({"unit":ally, "move":ally.moves[0]} for ally in allies)
            case "other_allies_basic":
                moves.extend({"unit":ally, "move":ally.moves[0]} for ally in allies if ally is not unit)
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
Telekinesis      = Move("Telekinesis",  0, ignore_defense=True,
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
                                 {"phase":"before_hit", "scope":"per_cast", "type":"cooldowns", "targets":"self", "moves":[], "turns_number":-10},
                                 {"phase":"after_ability", "scope":"per_cast", "type":"call", "targets":"enemy_target", "moves":[], "conditions":[{"has_used_ability_this_turn":False}]}])

Force_Grip       = Move("Force Grip", 3,
                        effects=[{"phase":"before_hit", "scope":"per_cast", "type":"bonus", "targets":"self", "conditions":[{"targets":"enemy_target", "status":others.Armor_Shred}], "critical_hit":True},
                                 {"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"all_enemies", "scaling":"self_physical_damage", "damage_base":3.0,"damage_variance":0.05},
                                 {"phase":"after_hit", "scope":"per_target", "type":"debuff", "targets":"all_enemies", "kind":debuffs.Daze.copy(duration=2)},
                                 {"phase":"before_hit", "scope":"per_cast", "type":"cooldowns", "targets":"self", "moves":[], "turns_number":-10},
                                 {"phase":"after_ability", "scope":"per_cast", "type":"call", "targets":"enemy_target", "moves":[Sundering_Strike], "conditions":[{"has_used_ability_this_turn":False}]}])

Sundering_Strike.effects[3]["moves"] = [Force_Grip]
Sundering_Strike.effects[4]["moves"] = [Force_Grip]
Telekinesis.effects[2]["moves"]      = [Sundering_Strike, Force_Grip]
Force_Grip.effects[3]["moves"]       = [Sundering_Strike]

#Jedi_Consular
Attack_As_Defense = Move("Attack As Defense", 3,
                         effects=[{"phase":"before_hit", "scope":"per_cast", "type":"ignore_defense", "targets":"self", "conditions":[{"chance":0.5}], "ignore_defense":True},
                                  {"phase":"on_hit", "scope":"per_target", "type":"special", "targets":"enemy_target", "scaling":"self_special_damage", "damage_base":1.448,"damage_variance":0.05},
                                  {"phase":"after_hit", "scope":"per_target", "type":"healing", "targets":"self", "healing_from_damage_percent":0.3}])

Jedi_Healing      = Move("Jedi Healing", 5,
                         effects=[{"phase":"on_hit", "scope":"per_target", "type":"healing", "targets":"all_allies", "scaling":"self_max_health", "damage_base":0.4,"damage_variance":0},
                                  {"phase":"after_ability", "scope":"per_cast", "type":"turn_meter", "targets":"self", "conditions":[{"chance":0.5}], "turn_meter_number":0.25}])

Saber_Strike      = Move("Saber Strike", 0,
                         effects=[{"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"enemy_target", "scaling":"self_physical_damage", "damage_base":2.2,"damage_variance":0.05},
                                  {"phase":"after_ability", "scope":"per_cast", "type":"cooldowns", "targets":"self", "moves":[Jedi_Healing, Attack_As_Defense], "conditions":[{"chance":0.5}], "turns_number":-1}])

#Kit_Fisto
Lightsaber_Mastery = Move("Lightsaber Mastery", 0,
                          effects=[{"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"enemy_target", "scaling":"self_physical_damage", "damage_base":1.468, "damage_variance":0.05},
                                   {"phase":"after_hit", "scope":"per_target", "type":"turn_meter", "targets":"self", "turn_meter_number":0.15, "conditions":[{"chance":0.5}]},
                                   {"phase":"after_ability", "scope":"per_cast", "type":"call", "targets":"self", "moves":[], "conditions":[{"chance":0.3}]}])
Lightsaber_Mastery.effects[2]["moves"] = [Lightsaber_Mastery]

# Note: Recursive call for Lightsaber Mastery might need handling in "call" effect type if strings are allowed or if I need object ref. 
# "moves" usually takes list of Move objects. I cannot reference Lightsaber_Mastery while defining it. 
# Solution: Define it first, then update it? Or use a separate Move object for the bonus attack if it's identical? 
# Or relies on the engine's "call" handling. Engine `apply_ability` -> `case "call":` -> `for move in temp_effect["moves"]: ... self.apply_ability(..., move)`.
# If I pass a string, the engine might fail if it expects objects. 
# Let's check `units.py` line 311 `for move in temp_effect["moves"]:`
# It iterates. If it's a string, it will crash or treat string as move? `apply_ability` expects `attacking_move` object.
# I need to pass the object. But I can't reference it yet.
# I will define `Lightsaber_Mastery` then update its `effects`.

Turn_the_Tide     = Move("Turn the Tide", 4,
                         effects=[{"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"all_enemies", "scaling":"self_physical_damage", "damage_base":1.29, "damage_variance":0.05},
                                  {"phase":"after_ability", "scope":"per_cast", "type":"buff", "targets":"all_allies", "kind":buffs.Potency_Up.copy(duration=3)}])

# Eeth_Koth
Breaching_Strike = Move("Breaching Strike", 0,
                        effects=[
                            {"phase":"on_hit", "scope":"per_target", "type":"physical", "targets":"enemy_target", "scaling":"self_physical_damage", "damage_base":1.539, "damage_variance":0.05},
                            {"phase":"after_hit", "scope":"per_target", "type":"debuff", "targets":"enemy_target", "kind":debuffs.Defense_Down.copy(duration=3), "conditions":[{"chance":0.5}]},
                            {"phase":"after_hit", "scope":"per_target", "type":"debuff", "targets":"enemy_target", "kind":debuffs.Defense_Down.copy(duration=3), "conditions":[{"targets":"enemy_target", "tags":["droid"]}]}
                        ])

Force_Push        = Move("Force Push", 3,
                        effects=[
                            {"phase":"on_hit", "scope":"per_target", "type":"special", "targets":"enemy_target", "scaling":"self_special_damage", "damage_base":1.391, "damage_variance":0.05},
                            {"phase":"after_hit", "scope":"per_target", "type":"debuff", "targets":"enemy_target", "kind":debuffs.Stun.copy(duration=1), "conditions":[{"chance":0.75}]},
                            {"phase":"after_hit", "scope":"per_target", "type":"debuff", "targets":"enemy_target", "kind":debuffs.Ability_Block.copy(duration=3), "conditions":[{"targets":"enemy_target", "tags":["droid"]}]}
                        ])
