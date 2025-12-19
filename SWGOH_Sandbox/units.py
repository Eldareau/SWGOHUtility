import random
import moves
import buffs
import others
import debuffs
import uniques
import leaders

def flat_defense_to_percent (flat_defense):
    defense_percent = ((flat_defense*100)/(flat_defense + 85 * 7.5))/100
    return defense_percent

def percent_defense_to_flat (percent_defense):
    return (percent_defense*100 * (85 * 7.5))/(100 - percent_defense*100)

def effects_to_keep(effects):
    effects_to_keep = []
    for effect in effects:
        if effect.duration > 0:
            effect.duration -= 1
            if effect.duration == 0:
                continue
        effects_to_keep.append(effect)
    return effects_to_keep

class Unit :
    def __init__(self, name, relic,
                 max_health, max_protection, speed, critical_damage, potency, tenacity, health_steal, defense_penetration,
                 physical_damage, physical_critical_chance, physical_armor_penetration, physical_accuracy, physical_armor, physical_dodge_rating, physical_critical_avoidance,
                 special_damage, special_critical_chance, special_resistance_penetration, special_accuracy, special_resistance, special_deflection_rating, special_critical_avoidance,
                 tags, role, side, moves=None, buffs=None, debuffs=None, others=None, turn_meter=0, is_galactic_legend=False, is_revivable=True) :
        
        self.name                = name
        self.relic               = relic

        self.max_health          = max_health
        self.max_protection      = max_protection
        self.speed               = speed
        self.critical_damage     = critical_damage
        self.potency             = potency
        self.tenacity            = tenacity
        self.health_steal        = health_steal
        self.defense_penetration = defense_penetration

        self.physical_damage             = physical_damage
        self.physical_critical_chance    = physical_critical_chance
        self.physical_armor_penetration  = physical_armor_penetration
        self.physical_accuracy           = physical_accuracy
        self.physical_armor              = physical_armor
        self.physical_dodge_rating       = physical_dodge_rating
        self.physical_critical_avoidance = physical_critical_avoidance

        self.special_damage                 = special_damage
        self.special_critical_chance        = special_critical_chance
        self.special_resistance_penetration = special_resistance_penetration
        self.special_accuracy               = special_accuracy
        self.special_resistance             = special_resistance
        self.special_deflection_rating      = special_deflection_rating
        self.special_critical_avoidance     = special_critical_avoidance

        self.base_speed = speed

        self.tags           = tags
        self.role           = role
        self.side           = side
        self.moves          = moves if moves is not None else []
        self.buffs          = buffs if buffs is not None else []
        self.debuffs        = debuffs if debuffs is not None else []
        self.others         = others if others is not None else []
        self.uniques        = []
        self.leader         = None
        self.turn_meter     = turn_meter
        self.health         = max_health
        self.protection     = max_protection
        self.counter_chance = 0.0

        self.has_used_ability_this_turn = False
        self.in_his_turn                = False
        self.is_galactic_legend         = is_galactic_legend
        self.is_revivable               = is_revivable
        self.hp_lock                    = False
        self.untargetable               = False
        self.cant_be_crit               = False
        self.dead                       = False

    def __str__(self):
        return f"{self.name}, Health: {self.health}, Protection: {self.protection}, Turn_Meter: {self.turn_meter}, Buffs: {self.buffs}, Debuffs: {self.debuffs}, Others: {self.others}"
    
    def get_teams(self, defending_team, attacking_team):
        if self in defending_team:
            return {"allies" : [u for u in defending_team if u is not self], "enemies" : attacking_team}
        else:
            return {"allies" : [u for u in attacking_team if u is not self], "enemies" : defending_team}
    
    def dispel_all_debuffs(self):
        for debuff in self.debuffs:
            if "dispellable" not in debuff.cant_be:
                self.remove_debuff(debuff)

    def manipulate_turn_meter(self, percent):
        turn_meter_amount = percent * 1000
        self.turn_meter += turn_meter_amount

        if self.turn_meter < 0 :
            self.turn_meter = 0
        # elif self.turn_meter > 1000 :
        #     self.turn_meter = 0
        #     game.take_a_turn(self)

    def manipulate_offense_stacking(self, percent):
        self.physical_damage *= (1 + percent)
        self.special_damage  *= (1 + percent)

    def manipulate_max_health(self, percent):
        delta = round(self.max_health * percent)
        self.max_health = max(1, self.max_health + delta)
        self.health = min(self.health, self.max_health)
    
    def register_uniques(self, game):
        for unique in self.uniques:
            unique.register(self, game)

    def register_leader(self, game):
        self.leader.register(self, game)

    def has_buff(self, buff_input=None):
        if buff_input is None:
            return len(self.buffs) > 0
        return any(buff == buff_input for buff in self.buffs)
    
    def has_debuff(self, debuff_input=None):
        if debuff_input is None:
            return len(self.debuffs) > 0
        return any(debuff == debuff_input for debuff in self.debuffs)
    
    def has_other(self, other_input=None):
        if other_input is None:
            return len(self.others) > 0
        return any(other == other_input for other in self.others)

    def add_move(self, move, stat):
        move.base_stat = stat
        self.moves.append(move)

    def remove_move(self, move):
        if move in self.moves:
            self.moves.remove(move)

    def add_debuff(self, new_debuff):
        for debuff in self.debuffs:
            if debuff.kind == new_debuff.kind:
                if "stackable" in new_debuff.cant_be:
                    # if the new debuff is the same AND has a longer duration, update it
                    if debuff.duration < new_debuff.duration:
                        debuff.duration = new_debuff.duration
                    return
        self.debuffs.append(new_debuff)

    def remove_debuff(self, debuff):
        if debuff in self.debuffs:
            self.debuffs.remove(debuff)

    def add_buff(self, new_buff):
        for buff in self.buffs:
            if buff.kind == new_buff.kind:
                if "stackable" in new_buff.cant_be:
                    # if the new buff is the same AND has a longer duration, update it
                    if buff.duration < new_buff.duration:
                        buff.duration = new_buff.duration
                    return
        self.buffs.append(new_buff)

    def remove_buff(self, buff):
        if buff in self.buffs:
            self.buffs.remove(buff)

    def add_other(self, new_other):
        for other in self.others:
            if other.kind == new_other.kind:
                if "stackable" in new_other.cant_be:
                    # if the new other is the same AND has a longer duration, update it
                    if other.duration < new_other.duration:
                        other.duration = new_other.duration
                    return
        self.others.append(new_other)

    def remove_other(self, other):
        if other in self.others:
            self.others.remove(other)

    def remove_everything(self):
        self.buffs   = []
        self.others  = []
        self.debuffs = []

    def on_turn_start(self, game):
        game.trigger_event("on_turn_start", targets=self, allies=self.get_teams(game.attacking_team, game.defending_team)["allies"])
        self.in_his_turn                = True
        return not self.has_debuff(debuffs.Stun)

    def on_turn_end(self, game):
        game.trigger_event("on_turn_end", targets=self)
        for move in self.moves:
            move.cooldown = max(0, move.cooldown - 1)
        self.debuffs     = effects_to_keep(self.debuffs)
        self.buffs       = effects_to_keep(self.buffs)
        self.others      = effects_to_keep(self.others)
        self.in_his_turn = False
        self.has_used_ability_this_turn = False

    def replace_target(self, targets, attacking_unit, defending_team, attacking_team):
        match(targets):
            case "all_allies":
                return attacking_team
            case "all_other_allies":
                return [ally for ally in attacking_team if ally is not attacking_unit]
            case "enemy_target":
                return [self]
            case "ally_target":
                return [self]
            case "all_enemies":
                return defending_team
            case "self":
                return [attacking_unit]
            
    def debuff_inflicted (self, attacking_unit, effect):
        if "kind" in effect and "resistible" in effect["kind"].cant_be:
            return True
        else:
            return random.random() <= max(0, attacking_unit.potency - self.tenacity) and not self.has_other(others.Cover)

    def check_tag_conditions(self, targets, tags):
        for tag in tags:
            if not all(tag in unit.tags for unit in targets):
                return False
        return True
    
    def check_status_conditions(self, targets, status):
        if str(status) == "debuffed":
            if not all(unit.has_debuff() for unit in targets):
                    return False
        else:
            if all(unit.has_debuff(status) for unit in targets):
                return True
            if all(unit.has_buff(status) for unit in targets):
                return True
            if all(unit.has_other(status) for unit in targets):
                return True
            return False
        return True

    def check_conditions(self, conditions, attacking_unit):
        for cond in conditions:
            match(cond):
                case {"targets": targets, "tags" : tags}:
                    return self.check_tag_conditions(targets, tags)
                case {"targets":targets, "status" : status}:
                    return self.check_status_conditions(targets, status)
                case {"has_used_ability_this_turn": has_used_ability_this_turn}:
                    return attacking_unit.has_used_ability_this_turn == has_used_ability_this_turn
                case {"in_his_turn": in_his_turn}:
                    return attacking_unit.in_his_turn == in_his_turn
                case {"chance": chance}:
                    return random.random() <= chance
               
    def apply_effect(self, game, effect, attacking_unit, attacking_move, total_damage=0):
        defending_team, attacking_team = game.get_teams(self)
        effect["targets"] = self.replace_target(effect["targets"], attacking_unit, defending_team, attacking_team)
        if "conditions" in effect:
                for condition in effect["conditions"]:
                    if "targets" in condition:
                        condition["targets"] = self.replace_target(condition["targets"], attacking_unit, defending_team, attacking_team)
                # if conditions are not met, effect is not applied
                if not(self.check_conditions(effect["conditions"], attacking_unit)):
                    return

        teams = attacking_unit.get_teams(game.attacking_team, game.defending_team)

        match (effect["type"]):
            case "debuff":
                if self.debuff_inflicted(attacking_unit, effect):
                    for _ in range(effect.get("stacks", 1)):
                        self.add_debuff(effect["kind"].copy(duration=effect["kind"].duration))
                else:
                    print(f"{self.name} resisted the " + str(effect["kind"]) + " !")
            case "buff":
                if not self.has_debuff(debuffs.Buff_Immunity) and not self.has_other(others.Cover):
                    for _ in range(effect.get("stacks", 1)):
                        game.trigger_event("on_gain_buff", targets=self, enemies=teams["enemies"], allies=teams["allies"])
                        self.add_buff(effect["kind"].copy(duration=effect["kind"].duration))
            case "other":
                for _ in range(effect.get("stacks", 1)):
                    self.add_other(effect["kind"].copy(duration=effect["kind"].duration))
            case "call":
                if not attacking_unit.has_debuff(debuffs.Daze):
                    for move in effect["moves"]:
                        if "self" in effect:
                            ## TODO implement calling move on another unit
                            pass
                        else:
                            # /!\ I MADE THE ASSUMPTION THAT IF THE MOVE CALLED HAS NO UNIT TAGGED WITH, IT MUST BE BECAUSE IT IS THE SAME UNIT CALLING IT /!\
                            self.apply_ability(game, attacking_unit, move)
            case "bonus":
                match (effect):
                    case {"defense_penetration_multiplier": defense_penetration_multiplier}:
                        attacking_move.defense_penetration *= defense_penetration_multiplier
                        print("x" + str(defense_penetration_multiplier) + " defense_penetration_multiplier has been applied (" + str(attacking_move.defense_penetration) + ")")
                    case {"bonus_damage_multiplier": bonus_damage_multiplier}:
                        attacking_move.damage_multiplier += bonus_damage_multiplier
                        print(str(bonus_damage_multiplier*100) + "% bonus_damage_multiplier has been applied")
                    case {"critical_chance": critical_chance}:
                        attacking_move.critical_chance += critical_chance
                        print(str(critical_chance) + "% critical_chance has been applied")
                    case {"max_health": max_health}:
                        self.manipulate_max_health(max_health)
                        print(str(max_health*100) + "% max_health has been applied to " + str(self.name))
            case "cooldowns":
                for move in effect["moves"]:
                    move.cooldown = max(0, move.cooldown + effect["turns_number"])
                print("Cooldowns have been modified by " + str(effect["turns_number"]) + " turn(s)")
            case "turn_meter":
                if (effect["turn_meter_number"] > 0 and not self.has_debuff(debuffs.Daze)) or (effect["turn_meter_number"] < 0 and self.debuff_inflicted(attacking_unit, effect)) :
                    self.manipulate_turn_meter(effect["turn_meter_number"])
                    print(f"{self.name}'s turn meter changed by {effect['turn_meter_number']*100}%")
                else:
                    print(f"{self.name} resisted turn meter removal !")
            case "healing":
                if "healing_from_damage_percent" in effect:
                    healing_amount = round(total_damage * effect["healing_from_damage_percent"])
                    attacking_unit.apply_healing(healing_amount)
            case "ignore_defense":
                attacking_move.ignore_defense = True
                print(f"{attacking_move.name} will ignore defense.")
            case _:
                print("Effect type " + effect["type"] + " not implemented yet.")
                
    def apply_before_effects(self, game, attacking_unit, main_target, attacking_move):
        game.trigger_event("on_before_attack", attacker=attacking_unit, targets=self, allies=attacking_unit.get_teams(game.attacking_team, game.defending_team)["allies"])
        game.trigger_event("on_before_attacked", attacker=attacking_unit, move=attacking_move)
        for effect in attacking_move.before_effects:
                self.apply_effect(game, effect, attacking_unit, attacking_move)

    def apply_during_effects(self, game, attacking_unit, main_target, attacking_move):
        game.trigger_event("on_during_attack", attacker=attacking_unit, targets=self)
        game.trigger_event("on_during_attacked", attacker=attacking_unit, allies=attacking_unit.get_teams(game.attacking_team, game.defending_team)["allies"], move=attacking_move, targets=self)
        for effect in attacking_move.during_effects:
                self.apply_effect(game, effect, attacking_unit, attacking_move)

    def apply_after_effects(self, game, attacking_unit, main_target, attacking_move, total_damage):
        game.trigger_event("on_after_attack", attacker=attacking_unit, targets=self)
        game.trigger_event("on_after_attacked", attacker=attacking_unit, allies=attacking_unit.get_teams(game.attacking_team, game.defending_team)["allies"], move=attacking_move, targets=self)
        for effect in attacking_move.after_effects:
                self.apply_effect(game, effect, attacking_unit, attacking_move, total_damage)

    def get_effective_physical_armor(self):
        effective_armor = self.physical_armor
        for _ in self.others:
            if self.has_other(others.Armor_Shred):
                effective_armor *= 0.5
        if self.has_debuff(debuffs.Defense_Down):
            effective_armor *= 0.5
        if self.has_buff(buffs.Defense_Up):
            effective_armor *= 1.5
        return effective_armor

    def get_effective_special_resistance(self):
        effective_resistance = self.special_resistance
        for _ in self.others:
            if self.has_other(others.Armor_Shred):
                effective_resistance *= 0.5
        if self.has_debuff(debuffs.Defense_Down):
            effective_resistance *= 0.5
        if self.has_buff(buffs.Defense_Up):
            effective_resistance *= 1.5
        return effective_resistance
    
    def apply_healing(self, healing_amount):
        if not self.has_debuff(debuffs.Healing_Immunity):
            self.health = min(self.max_health, self.health + healing_amount)
            print(self.name + " + " + str(healing_amount) + " !")

    def update_scaling_for_moves(self, effect):
        if "scaling" in effect:
            match(effect["scaling"]):
                case ("self_physical_damage", _):
                    effect["scaling"] = ("self_physical_damage", self.physical_damage)
                case ("self_special_damage", _):
                    effect["scaling"] = ("self_special_damage", self.special_damage)
                case ("self_max_health", _):
                    effect["scaling"] = ("self_max_health", self.max_health)
                case _:
                    raise Exception("Effect scaling isn't implmented yet. (" + str(effect) +")")
    
    def apply_damage(self, game, attacking_unit, attacking_move, effect):
        variation = 1 + random.uniform(-effect["damage_variance"], effect["damage_variance"])
        # print(attacking_movebase_stat)
        # print(attacking_movedamage)
        # print(variation)
        total = max(1, effect["scaling"][1] * effect["damage_base"] * variation)
        # print("base dmg : " + str(total))
        total *= attacking_move.damage_multiplier
        # print("after dmg multiplier dmg : " + str(total))

        if effect["type"] == "physical":
            defense = self.get_effective_physical_armor()
            critical_chance = attacking_unit.physical_critical_chance
            crit_avoidance = self.physical_critical_avoidance
            penetration = attacking_unit.physical_armor_penetration
        elif effect["type"] == "special":
            defense = self.get_effective_special_resistance()
            critical_chance = attacking_unit.special_critical_chance
            crit_avoidance = self.special_critical_avoidance
            penetration = attacking_unit.special_resistance_penetration

        if not attacking_move.ignore_defense:
            attacker_penetration = penetration * (1 + attacking_unit.defense_penetration + attacking_move.defense_penetration)
            final_defense        = percent_defense_to_flat(defense) - percent_defense_to_flat(attacker_penetration)
            total = max(1, total * (1 - (max(0, flat_defense_to_percent(final_defense)))))
        
        if not self.has_buff(buffs.Critical_Hit_Immunity) and not self.cant_be_crit:
            if attacking_unit.has_buff(buffs.Advantage) or self.has_debuff(debuffs.Vulnerable) or random.random() <= max(0, (critical_chance + attacking_move.critical_chance) - crit_avoidance):
                total *= attacking_unit.critical_damage
                print("Critical hit ! (x" + str(attacking_unit.critical_damage) + ")")
                game.trigger_event("on_crit", attacker=attacking_unit, targets=self)
                game.trigger_event("on_crited", targets=self)

        if not(attacking_unit.has_debuff(debuffs.Healing_Immunity)):
            healing_amount = round(attacking_unit.health_steal * total)
            attacking_unit.apply_healing(healing_amount)

        total = round(total)
        print(total)
        protection_overflow = self.protection - total
        self.protection = max(0, protection_overflow)
        if not self.hp_lock and protection_overflow < 0:
            self.health = max(0, self.health + protection_overflow)
        print(self.name + " - " + str(total) + " !")
        print(self)
        attacking_move.reset_temporary_modifiers()
        return total

    def apply_ability(self, game, attacking_unit, attacking_move, main_target = False):
        
        per_target_effects    = [effect for effect in attacking_move.effects if effect["scope"]=="per_target"]
        before_hit_effects    = [effect for effect in attacking_move.effects if effect["phase"]=="before_hit"]
        on_hit_effects        = [effect for effect in attacking_move.effects if effect["phase"]=="on_hit"]
        after_hit_effects     = [effect for effect in attacking_move.effects if effect["phase"]=="after_hit"]
        after_ability_effects = [effect for effect in attacking_move.effects if effect["phase"]=="after_ability"]

        print(attacking_unit.name + " used " + attacking_move.name)
        
        evaded = False
        attacking_unit.has_used_ability_this_turn = False
        total_ability_damage = 0

        for effect in attacking_move.effects:
            attacking_unit.update_scaling_for_moves(effect)
            if effect in per_target_effects and effect in before_hit_effects:
                print(effect)
                self.apply_effect(game, effect, self, attacking_move)
            if effect in per_target_effects and effect in on_hit_effects:
                print(effect)
                if effect["type"] in ["physical", "special"] and not (self.has_buff(buffs.Damage_Immunity) or self.has_other(others.Cover)):
                    if "cant_be" in effect and not("evaded" in effect["cant_be"]):
                        if self.has_buff(buffs.Foresight):
                            evaded = True
                            self.remove_buff(buffs.Foresight)
                        else:
                            evaded |= effect["type"] == "Physical" and random.random() <= max(0.02, self.physical_dodge_rating - attacking_unit.physical_accuracy)
                            evaded |= effect["type"] == "Special" and random.random() <= max(0.02, self.special_deflection_rating - attacking_unit.special_accuracy)
                    if not evaded:
                        total_ability_damage += self.apply_damage(game, attacking_unit, attacking_move, effect)
                        if self.health <= 0:
                            self.dead = True
                            game.trigger_event("on_death", game=game, targets=self, allies=self.get_teams(game.attacking_team, game.defending_team)["allies"])
                        elif random.random() <= self.counter_chance and ("cant_be" in effect and not "countered" in effect["cant_be"]) and not self.has_debuff(debuffs.Daze) and attacking_unit.in_his_turn:
                            selected_enemy = game.choose_targets(game.attacking_team, attacking_unit)
                            selected_enemy.apply_ability(game, self, self.moves[0])
                elif effect["type"] == "healing" and not self.has_debuff(debuffs.Healing_Immunity):
                    healing_amount = round(effect["scaling"] * effect["damage_base"])
                    self.apply_healing(healing_amount)
                else:
                    raise Exception("Effect must have physical, special or healing type to be in on hit phase")
            if effect in per_target_effects and effect in after_hit_effects and total_ability_damage > 0:
                print(effect)
                self.apply_effect(game, effect, self, attacking_move, total_ability_damage)
            if effect in per_target_effects and effect in after_ability_effects:
                print(effect)
                attacking_unit.has_used_ability_this_turn = True
                self.apply_effect(game, effect, self, attacking_move)

        attacking_move.cooldown = attacking_move.max_cooldown

    def resolve_targets(self, game, effect):
        print(effect)
        match(effect["targets"]):
            case "enemy_target":
                target = game.choose_targets(game.defending_team)
                return [target], target
            case "ally_target":
                target = game.choose_targets(game.attacking_team)
                return [target], target
            case "all_enemies":
                target = game.choose_targets(game.defending_team)
                return game.defending_team, target
            case "all_allies":
                return game.attacking_team, self ## maybe wrong to assume self is the main target here
            case "self":
                return [self], self

        raise ValueError(f"Unknown target type: {effect}")

    def complete_turn (self, game, selected_move=None) :
        print(self.name + " is taking a turn. Select an ennemy to attack:")
        selected_move  = game.choose_move(self)

        per_cast_effects      = [effect for effect in selected_move.effects if effect["scope"]=="per_cast"]
        before_hit_effects    = [effect for effect in selected_move.effects if effect["phase"]=="before_hit"]
        after_ability_effects = [effect for effect in selected_move.effects if effect["phase"]=="after_ability"]
        on_hit_effects        = [effect for effect in selected_move.effects if effect["phase"]=="on_hit"]

        targets, main_target = self.resolve_targets(game, on_hit_effects[0])

        for effect in selected_move.effects:
            if effect in per_cast_effects and effect in before_hit_effects:
                print(effect)
                for unit in targets:
                    unit.apply_effect(game, effect, self, selected_move)
        for target in targets:
            target.apply_ability(game, self, selected_move, unit is main_target)
        for effect in selected_move.effects:
            if effect in per_cast_effects and effect in after_ability_effects:
                print(effect)
                for unit in targets:
                    unit.apply_effect(game, effect, self, selected_move)

    def take_a_turn(self, game):
        game.swap_teams_if_needed(self)
        if self.on_turn_start(game):
            self.complete_turn(game)
        self.on_turn_end(game)
        game.compute_combat_over()

#                                          Relic, HP   ,  PROT, SPD, CD  , POT , TEN , HS  , DP , PDMG, PCC   , PAP, PACC, PARM , PDDG, PCA , SDMG, SCC   , SRP, SACC, SRes , SDFL, SCA , tags, role, side
General_Grievous  = Unit("General Grievous",   8, 79509, 48053, 129, 1.68, 0.31, 0.42, 0.20, 0.0, 6346, 0.8196, 205, 0.00, 0.484, 0.02, 0.00, 5661, 0.2842, 000, 0.00, 0.370, 0.02, 0.00, ["leader", "droid", "separatist", "fleet_commander"], "attacker", "dark_side")
General_Grievous.add_move(moves.Furious_Assault, General_Grievous.max_health)
General_Grievous.add_move(moves.Grievous_Wounds, General_Grievous.max_health)
General_Grievous.add_move(moves.Skittering_Horror, General_Grievous.max_health)

General_Skywalker = Unit("General Skywalker",  8, 67264, 64188, 157, 1.50, 0.65, 0.63, 0.30, 0.0, 7038, 0.6467, 316, 0.18, 0.539, 0.02, 0.00, 6086, 0.1000, 120, 0.18, 0.297, 0.02, 0.00, ["leader", "501st", "galactic_republic", "jedi"], "attacker", "light_side")
General_Skywalker.add_move(moves.Furious_Slash, General_Skywalker.physical_damage)
General_Skywalker.add_move(moves.Sundering_Strike, General_Skywalker.physical_damage)
General_Skywalker.add_move(moves.Force_Grip, General_Skywalker.physical_damage)
moves.Telekinesis.base_stat = General_Skywalker.physical_damage
General_Skywalker.leader = leaders.general_of_the_501st()
General_Skywalker.uniques.append(uniques.the_chosen_one())
General_Skywalker.uniques.append(uniques.hero_with_no_fear())

Jedi_Consular     = Unit("Jedi Consular",      8, 72323, 35447, 139, 1.50, 0.13, 0.45, 0.15, 0.0, 4797, 0.5030, 46 , 0.00, 0.503, 0.02, 0.18, 7382, 0.1750, 142, 0.00, 0.445, 0.02, 0.18, ["jedi", "galactic_republic", "jedi_vanguard", "order_66_raid"], "healer", "light_side")
Jedi_Consular.add_move(moves.Saber_Strike, Jedi_Consular.physical_damage)
Jedi_Consular.add_move(moves.Jedi_Healing, Jedi_Consular.max_health)
Jedi_Consular.add_move(moves.Attack_As_Defense, Jedi_Consular.special_damage)
Jedi_Consular.add_debuff(debuffs.Healing_Immunity.copy(duration=2))

