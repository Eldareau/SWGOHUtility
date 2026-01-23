
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust path to import modules from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import units
import moves
import buffs
import debuffs
import leaders
import uniques
from main import Game

class TestImaGunDi(unittest.TestCase):
    def setUp(self):
        self.igd = units.Ima_Gun_Di
        self.dummy_ally = units.Kit_Fisto # Jedi Ally
        self.dummy_enemy = units.General_Grievous # Droid Enemy
        self.dummy_enemy_non_droid = units.General_Skywalker # Non-Droid Enemy
        
        # Reset states
        self.igd.health = self.igd.max_health
        self.igd.turn_meter = 0
        self.igd.remove_everything()
        self.igd.potency = 1.0 # Ensure debuffs land
        self.igd.reset_cooldowns = lambda: [setattr(m, 'cooldown', 0) for m in self.igd.moves]
        self.igd.reset_cooldowns()
        
        self.dummy_ally.remove_everything()
        
        self.dummy_enemy.health = self.dummy_enemy.max_health
        self.dummy_enemy.remove_everything()
        
        self.dummy_enemy_non_droid.health = self.dummy_enemy_non_droid.max_health
        self.dummy_enemy_non_droid.remove_everything()

        self.team = [self.igd, self.dummy_ally]
        self.enemy_team = [self.dummy_enemy, self.dummy_enemy_non_droid]
        self.game = Game(self.team, self.enemy_team)
        self.game.compute_first_swap()

    def test_sunder_basic_vs_droid(self):
        """
        Test Sunder (Basic) vs Droid:
        - 100% More Damage (Bonus)
        - 100% Defense Down Chance
        """
        # Sunder is move 0
        move = self.igd.moves[0]
        
        # Mock random to ensure no dodge/crit interference if possible, 
        # but we mainly check logic application.
        # "100% chance" conditions in code relies on tags, so random shouldn't matter for the condition check itself.
        
        
        with patch('random.random', side_effect=[0.5, 0.5, 0.5, 0.5]): 
            # Droid Target
            # We need to spy on apply_damage to verify bonus multiplier?
            # Or check debuffs.
            
            # The "before_hit" bonus applies +1.0 multiplier.
            # Base multiplier is 1.899. Total should be 2.899?
            # Or adds to move.damage_multiplier of 1.
            # `units.py` line 330: attacking_move.damage_multiplier += bonus_damage_multiplier
            # Default Move.damage_multiplier is 1.
            # NO. `units.py` `add_move` does NOT set damage_multiplier. `Move` init sets it.
            # `Move` init defaults to 1? NO. `Move` init takes `damage_multiplier` arg.
            # Sunder defined as `damage_multiplier=1` (default) ? No wait.
            # `units.py` line 28: `self.damage_multiplier = self.base_damage_multiplier`
            # `Sunder` definition doesn't specify `damage_multiplier` argument in `Move(...)`?
            # Let's check definition.
            # `Sunder(..., damage_multiplier=1.899, ...)` NO.
            # `Sunder = Move("Sunder", 0, effects=[...])`.
            # If `damage_multiplier` arg is missing, it defaults to 1.
            # BUT, the `damage_base` in effect is 1.899.
            # The `damage_multiplier` is a global scaler for the move usually related to Offense Stat?
            # In `units.py`: `total *= attacking_move.damage_multiplier`
            # If `main.py` applies bonus, it modifies `attacking_move.damage_multiplier`.
            
            # So if invalid target (Droid):
            # `before_hit` adds +1.0 to multiplier. Old = 1. New = 2.
            # Damage calculation: `damage_base` (1.899 * stat) * `damage_multiplier` (2).
            # So damage is DOUBLED. Correct (100% more).
            
            self.dummy_enemy.apply_ability(self.game, self.igd, move, main_target=True)
            # Cannot easily assert damage value without mocking everything, but check Debuff.
            
            self.assertTrue(self.dummy_enemy.has_debuff(debuffs.Defense_Down), "Droid should have Defense Down")

    def test_sunder_basic_vs_non_droid(self):
        """
        Test Sunder vs Non-Droid:
        - Normal Damage
        - 50% Defense Down Chance
        """
        move = self.igd.moves[0]
        
        # Case 1: Random < 0.5 (Proc)
        with patch('random.random', return_value=0.0):
             self.dummy_enemy_non_droid.apply_ability(self.game, self.igd, move, main_target=True)
             # Target is chosen by game.choose_targets mock? 
             # Wait, `apply_ability` resolves targets using `resolve_targets`.
             # `resolve_targets` calls `game.choose_targets`.
             # We need to mock `game.choose_targets`.
        
    def test_rebuke_special(self):
        """
        Test Rebuke (Special):
        - Grant Defense Up to all allies for 3 turns.
        """
        move = self.igd.moves[1]
        
        # Mock choose_targets to pick enemy
        
        # Mock choose_move (returns Rebuke = index 1) and choose_targets (returns enemy)
        # We also need to Mock `input` if `complete_turn` prints/waits?
        # `complete_turn` calls `choose_move` which calls `input`.
        # `game.choose_move` prints and `int(input())`.
        
        with patch('main.Game.choose_move', return_value=move), \
             patch('main.Game.choose_targets', return_value=self.dummy_enemy), \
             patch('builtins.print'):
             
             self.igd.complete_turn(self.game, selected_move=move)
        
        self.assertTrue(self.igd.has_buff(buffs.Defense_Up), "IGD should have Defense Up")
        self.assertTrue(self.dummy_ally.has_buff(buffs.Defense_Up), "Ally should have Defense Up")
        # Check duration?
        # Access buff directly to check duration
        buff = next(b for b in self.igd.buffs if b.kind == "defense up")
        self.assertEqual(buff.duration, 3)

    def test_jedi_strategist_leader(self):
        """
        Test Leader Ability:
        - +30 Flat Defense to All
        - +35% Counter Chance, +25% Counter Damage to Jedi
        """
        # Init Game triggers leader abilities
        # We need to check stats BEFORE and AFTER.
        # But `Game` init calls `match_init` which calls `apply_leader_abilities`.
        
        # Override leader
        self.igd.leader = leaders.jedi_strategist()
        self.team[0] = self.igd # make sure he is leader
        
        # Snapshot stats
        base_armor = self.dummy_ally.physical_armor # percent
        base_counter = self.dummy_ally.counter_chance
        base_counter_dmg = self.dummy_ally.counter_damage
        
        # Trigger manually
        self.igd.leader.register(self.igd, self.game)
        # Trigger event "on_leader_start_of_battle"
        self.game.trigger_event("on_leader_start_of_battle", leader=self.igd, allies=[self.dummy_ally], enemies=self.enemy_team)
        
        # Check Defense (Approximate due to flat->percent conversion)
        self.assertGreater(self.dummy_ally.physical_armor, base_armor, "Defense should increase")
        
        # Check Counter Chance (Jedi)
        self.assertAlmostEqual(self.dummy_ally.counter_chance, base_counter + 0.35, delta=0.01)
        self.assertAlmostEqual(self.dummy_ally.counter_damage, base_counter_dmg + 0.25, delta=0.01)

    def test_last_stand_unique(self):
        """
        Test Unique Ability:
        - When Crit: Gain 3-turn healing tracker.
        - On Turn Start: Heal 15% Max Health.
        """
        # 1. Trigger Crit
        # Manually invoke handler or simulate attack
        # Let's manually invoke for precision
        
        # Handler is registered?
        self.igd.register_uniques(self.game)
        
        # Fire 'on_crited'
        self.game.trigger_event("on_crited", targets=self.igd)
        
        # Check 'others' for tracker
        has_tracker = any(hasattr(o, 'name') and o.name == "LastStandHeal" for o in self.igd.others)
        self.assertTrue(has_tracker, "Should have LastStandHeal tracker after being crit")
        
        # 2. Trigger Turn Start -> Heal
        start_hp = self.igd.max_health * 0.5
        self.igd.health = start_hp
        
        # Fire 'on_turn_start'
        # The unique listens to 'on_turn_start' on game?
        # `uniques.py`: `def on_turn_start(game, targets, **kw):`
        # `units.py` `on_turn_start` triggers `game.trigger_event("on_turn_start", targets=self, ...)`
        
        self.igd.on_turn_start(self.game)
        
        expected_heal = round(self.igd.max_health * 0.15)
        self.assertEqual(self.igd.health, start_hp + expected_heal, "Should have healed 15% HP")

if __name__ == "__main__":
    unittest.main()
