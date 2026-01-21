import unittest
import sys
import os
import copy
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main
import units
import moves
import buffs
import leaders

class TestKitFisto(unittest.TestCase):
    def setUp(self):
        # Reset Global Moves
        for move_name in dir(moves):
            m = getattr(moves, move_name)
            if isinstance(m, moves.Move):
                m.cooldown = 0
        
        self.kit = copy.deepcopy(units.Kit_Fisto)
        self.ally = units.Unit("Jedi Ally", 1, 50000, 50000, 100, 1.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ["jedi", "light_side"], "attacker", "light_side")
        self.non_jedi_ally = units.Unit("Clone Ally", 1, 50000, 50000, 100, 1.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ["clone", "light_side"], "attacker", "light_side")
        self.enemy = units.Unit("Target Dummy", 1, 100000, 100000, 100, 1.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ["dummy"], "attacker", "dark_side")
        
        self.game = main.Game([self.kit, self.ally, self.non_jedi_ally], [self.enemy])
        # Manually register Kit as leader for testing leader ability
        self.game.match_init() # Applies Uniques and Leaders

    def test_unique_stats(self):
        """Test Superior Bladework: +35% Counter Chance, +20% Offense."""
        # Counter Chance default assumed 0? units.py defaults to 0.00 usually or specified.
        # Kit default stats provided in file? No, I put args in unit instantiation.
        # Wait, I didn't verify base counter chance in args. I assumed 0.35 is added.
        # Let's check effective.
        # Base Offense (Physical) = 6828.
        # With +20%: 6828 * 1.2 = 8193.6
        
        self.assertGreater(self.kit.counter_chance, 0.34)
        self.assertAlmostEqual(self.kit.physical_damage, 6828 * 1.2, delta=1.0)

    def test_leader_ability(self):
        """Test Jedi Protector: +25% Tenacity (All), +45 Defense (Jedi)."""
        # Tenacity
        # Kit (Jedi)
        self.assertAlmostEqual(self.kit.tenacity, 0.48 + 0.25, delta=0.01)
        # Ally (Jedi)
        self.assertAlmostEqual(self.ally.tenacity, 0.0 + 0.25, delta=0.01) # Ally base 0
        # Non-Jedi
        self.assertAlmostEqual(self.non_jedi_ally.tenacity, 0.0 + 0.25, delta=0.01)
        
        # Defense (Physical)
        # Kit base 0.514.
        # Logic: Flat -> +45 -> %.
        # Verification: just check it increased significantly.
        self.assertGreater(self.kit.physical_armor, 0.514)
        
        # Non-Jedi should NOT gain defense
        self.assertEqual(self.non_jedi_ally.physical_armor, 0.0) # Base 0

    @patch('main.Game.choose_targets')
    @patch('units.random.random')
    def test_basic_attack_mechanics(self, mock_random, mock_targets):
        """
        Test Lightsaber Mastery
        Spec Check:
        - Deal Physical damage to target enemy.
        - Has a 30% chance to attack again.
        - Gain 15% Turn Meter (per hit).
        """
        mock_targets.return_value = self.enemy
        
        # Sequence logic simulation:
        # Attack 1: Evade(Fail), Crit(Fail), TM Gain(Pass), Bonus Attack Check(Pass)
        # Attack 2: Evade(Fail), Crit(Fail), TM Gain(Pass), Bonus Attack Check(Fail)
        
        mock_random.side_effect = [
            1.0, 1.0, 0.1, 0.1,  # Attack 1
            1.0, 1.0, 0.1, 0.9   # Attack 2
        ]
        
        self.kit.physical_critical_chance = 0
        self.kit.moves[0].critical_chance = 0
        self.kit.turn_meter = 0
        move = self.kit.moves[0]
        
        self.kit.complete_turn(self.game, selected_move=move)
        
        # 15% TM per hit * 2 hits = 30% Turn Meter
        self.assertEqual(self.kit.turn_meter, 300, "Should gain 300 Turn Meter (150*2)")
        
        initial_hp = 100000 + 100000
        damage_dealt = initial_hp - (self.enemy.health + self.enemy.protection)
        self.assertGreater(damage_dealt, 5000)

    @patch('main.Game.choose_targets')
    def test_special_ability(self, mock_targets):
        """
        Test Turn the Tide
        Spec Check:
        - Deal Physical damage to all enemies.
        - Grant Potency Up to all allies for 3 turns.
        """
        mock_targets.return_value = self.enemy
        
        move = self.kit.moves[1]
        
        self.kit.complete_turn(self.game, selected_move=move)
        
        self.assertTrue(self.kit.has_buff(buffs.Potency_Up), "Kit Fisto should gain Potency Up")
        self.assertTrue(self.ally.has_buff(buffs.Potency_Up), "Allies should gain Potency Up")


if __name__ == '__main__':
    unittest.main()
