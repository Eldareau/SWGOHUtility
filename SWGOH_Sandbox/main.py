import units
import debuffs
import buffs
import others
import random

ally_units = [units.General_Grievous]
enemy_units = [units.General_Skywalker, units.Jedi_Consular]

GREY = "\033[90m"
RESET = "\033[0m"

class Game :
    def __init__(self, attacking_team, defending_team, turn_number=0):

        self.defending_team = defending_team
        self.attacking_team = attacking_team
        self.player_team    = attacking_team
        self.enemy_team     = defending_team

        self.turn_number   = turn_number
        self.game_over     = False

        self.listeners = []

    def trigger_event(self, event_name, **kwargs):
        for event, callback in self.listeners:
            if event == event_name:
                callback(**kwargs)
        
    def get_teams(self, defending_unit):
        if defending_unit in self.defending_team:
            return self.defending_team, self.attacking_team
        else:
            return self.attacking_team, self.defending_team
        
    def apply_unique_abilities(self) :
        print("Applying unique abilities...")
        # Enemies uniques are applied first
        for unit in self.defending_team:
            unit.register_uniques(self)
            self.trigger_event("on_unique_start_of_battle", unit=unit, allies=[u for u in self.defending_team if u is not unit])

        for unit in self.attacking_team:
            unit.register_uniques(self)
            self.trigger_event("on_unique_start_of_battle", unit=unit, allies=[u for u in self.attacking_team if u is not unit])

    def apply_leader_abilities(self) :
        print("Applying leader abilities...")
        # Ally leader is applied first
        attacking_leader = self.attacking_team[0]
        if attacking_leader.leader is not None:
            print("Registering attacking leader:", attacking_leader.leader.name)
            attacking_leader.register_leader(self)
            self.trigger_event("on_leader_start_of_battle", leader=attacking_leader, allies=[u for u in self.attacking_team if u is not attacking_leader], enemies=self.attacking_team)

        defending_leader = self.defending_team[0]
        if defending_leader.leader is not None:
            print("Registering attacking leader:", defending_leader.leader.name)
            defending_leader.register_leader(self)
            self.trigger_event("on_leader_start_of_battle", leader=defending_leader, allies=[u for u in self.defending_team if u is not defending_leader], enemies=self.attacking_team)

    def compute_first_swap(self):
        for unit in self.attacking_team + self.defending_team:
            for move in unit.moves:
                for effect in move.effects:
                    if "scaling" in effect:
                        match(effect["scaling"]):
                            case "self_physical_damage":
                                effect["scaling"] = ("self_physical_damage", unit.physical_damage)
                            case "self_special_damage":
                                effect["scaling"] = ("self_special_damage", unit.special_damage)
                            case "self_max_health":
                                effect["scaling"] = ("self_max_health", unit.max_health)
                            case _:
                                raise Exception("Effect scaling isn't implmented yet. (" + effect +")")

    def match_init(self):
# Base stats are determined by level, rarity, and current gear level of the unit.
# Then mods and datacrons are applied using the base stats for percent calculations and then they are all added together.[1]
# Stats from equipped Gear is then added. Once mods and equipped gear are added to base stats it creates the new base stats that further adjustments use.
# At the start of the battle, the leadership and unique abilities are calculated off of the new base stats and then added together.
#     Enemy Uniques (In order of placement)
#     Player Uniques (In order of placement)
#     Player Lead
#     Enemy Lead
# After unique abilities are applied any bonus mechanic, including those from Datacrons, will be applied.[2]

# 1	Base stats by level/gear/rarity
# 2	Mods & Datacron stat bonuses (percent / flat)
# 3	Gear bonuses (from equipped items)
# 4	Pre-battle Buffs (buffs that last encounter, e.g. relic deltas, mastery, gear relic bonuses)
# 5	Unique abilities (enemy uniques first, then ally uniques)
# 6	Leader abilities (ally lead, then enemy lead)
# 7	Finalize “starting stats” (HP, Protection, Offense, Defense, Speed, Potency, Tenacity, etc.)
# 8	Apply any “start-of-battle” effects that trigger on battle start (e.g. Lead buffs, some uniques, free TM, buff-on-spawn, etc.)
        self.apply_unique_abilities()
        self.apply_leader_abilities()
        self.compute_first_swap()

    def compute_turn_meter(self):
        units_to_take_a_turn = []
        for unit in self.defending_team + self.attacking_team:
            unit.turn_meter += unit.speed
            if unit.turn_meter >= 1000:
                unit.turn_meter -= 1000
                units_to_take_a_turn.append(unit)
        return units_to_take_a_turn
    
    def choose_targets(self, team_to_attack, countered_enemy=None) :
        print("Select an ennemy to attack:")
        alive_enemies   = [enemy for enemy in team_to_attack if not enemy.dead]
        priority_target = [enemy for enemy in alive_enemies if enemy.has_buff(buffs.Taunt) or enemy.has_other(others.Advance) or enemy.has_debuff(debuffs.Marked)]

        if priority_target:
            valid_targets = priority_target
        else:
            valid_targets = [enemy for enemy in alive_enemies if not (enemy.has_buff(buffs.Stealth) or enemy.has_other(others.Cover))]

        for i, unit in enumerate(team_to_attack):
            if unit in valid_targets:
                print(str(i) + " : " + str(unit))
            else:
                if unit.dead:
                    print(f"{GREY}{i} : {unit}{RESET}")
                else:
                    print(f"{i} : {unit}")

        if countered_enemy in valid_targets:
            return team_to_attack.index(countered_enemy)
        elif not countered_enemy == None:
            return team_to_attack.index(random.choice(team_to_attack))
        else:
            while True:
                try :
                    selected_enemy_index = int(input())
                    if 0 <= selected_enemy_index < len(team_to_attack) :
                        selected_enemy = team_to_attack[selected_enemy_index]
                        if selected_enemy in valid_targets :
                            return team_to_attack[selected_enemy_index]
                        else :
                            print("Invalid selection, please choose again.")
                    else :
                        print("Invalid selection, please choose again.")
                except ValueError:
                    print("Invalid selection, please choose again.")
        
    
    def choose_move(self, unit) :
        while True :
            print("Select a move to do :")
            if unit.has_debuff(debuffs.Ability_Block) :
                input("Ability Blocked! Using basic attack. Press Enter to continue...")
                return unit.moves[0]
            for i, move in enumerate(unit.moves):
                if move.cooldown > 0:
                    print(f"{GREY}{i} : {move}{RESET}")
                else:
                    print(f"{i} : {move}")
            selected_move_index = int(input())
            if unit.moves[selected_move_index].cooldown > 0:
                continue
            return unit.moves[selected_move_index]

    def swap_teams_if_needed(self, unit) :
        if unit in self.defending_team :
            temp = self.defending_team
            self.defending_team = self.attacking_team
            self.attacking_team = temp

    def compute_combat_over(self):
        if all(unit.dead for unit in self.player_team) :
            print("All ally units have been defeated. Combat over.")
            self.game_over = True
        elif all(unit.dead for unit in self.enemy_team) :
            print("All enemy units have been defeated. Combat over.")
            self.game_over = True

print("Combat Start")

game = Game(ally_units, enemy_units)
game.match_init()

while (not(game.game_over)):
    # compute which units have enough turn meter to take a turn
    units_to_take_a_turn = game.compute_turn_meter()
    for unit_i in range(len(units_to_take_a_turn)):
        if game.game_over:
            break
        # choose the unit with the highest turn meter to take a turn
        selected_unit = max(units_to_take_a_turn, key=lambda x: x.turn_meter)
        selected_unit.take_a_turn(game)
        del units_to_take_a_turn[units_to_take_a_turn.index(selected_unit)]
        

        
