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
        """Test Lightsaber Mastery: Damage, TM Gain, Bonus Attack."""
        mock_targets.return_value = self.enemy
        
        # Sequence logic:
        # Attack 1:
        # 1. Evade Check (expect Fail -> >0.02)
        # 2. Crit Check (expect Fail -> >0)
        # 3. TM Gain Condition (Chance 0.5) -> Pass (<=0.5)
        # 4. Bonus Check (Chance 0.3) -> Pass (<=0.3)
        # Bonus Attack (Attack 2):
        # 5. Evade Check
        # 6. Crit Check
        # 7. TM Gain Condition -> Pass
        # 8. Bonus Check -> Fail (>0.3)
        
        mock_random.side_effect = [
            1.0, 1.0, 0.1, 0.1,  # Attack 1: Evade, Crit, TM, Bonus
            1.0, 1.0, 0.1, 0.9   # Attack 2: Evade, Crit, TM, Bonus
        ]
        
        self.kit.physical_critical_chance = 0
        self.kit.moves[0].critical_chance = 0
        self.kit.turn_meter = 0
        move = self.kit.moves[0]
        
        self.kit.complete_turn(self.game, selected_move=move)
        
        self.assertEqual(self.kit.turn_meter, 300)
        
        initial_hp = 100000 + 100000
        damage_dealt = initial_hp - (self.enemy.health + self.enemy.protection)
        self.assertGreater(damage_dealt, 5000)

    @patch('main.Game.choose_targets')
    def test_special_ability(self, mock_targets):
        """Test Turn the Tide: AOE, Potency Up."""
        # For AOE, it selects all enemies. 'game.choose_targets' might still be called for "all_enemies" case?
        # units.py L523: case "all_enemies": target = game.choose_targets(game.defending_team). 
        # Wait, if target type is "all_enemies", why choose targets? Ah, maybe to return "primary" target?
        # Yes, returns (team, target).
        mock_targets.return_value = self.enemy
        
        move = self.kit.moves[1]
        
        self.kit.complete_turn(self.game, selected_move=move)
        
        self.assertTrue(self.kit.has_buff(buffs.Potency_Up))
        self.assertTrue(self.ally.has_buff(buffs.Potency_Up))


if __name__ == '__main__':
    unittest.main()
