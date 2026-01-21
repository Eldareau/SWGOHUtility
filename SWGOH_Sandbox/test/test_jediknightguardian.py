
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
import debuffs
import leaders
import uniques

class TestJediKnightGuardian(unittest.TestCase):
    def setUp(self):
        # Reset Global Moves
        for move_name in dir(moves):
            m = getattr(moves, move_name)
            if isinstance(m, moves.Move):
                m.cooldown = 0
        
        self.jkg = copy.deepcopy(units.Jedi_Knight_Guardian)
        self.enemy = units.Unit("Target Dummy", 1, 100000, 100000, 100, 1.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ["dummy"], "attacker", "dark_side")
        
        self.game = main.Game([self.jkg], [self.enemy])
        self.game.match_init() # Applies Uniques

    @patch('main.Game.choose_targets')
    @patch('units.random.random')
    def test_saber_sweep(self, mock_random, mock_targets):
        """
        Test Saber Sweep (Basic)
        Spec Check:
        - Deal Physical damage.
        - 55% chance to inflict Offense Down for 2 turns.
        """
        mock_targets.return_value = self.enemy
        
        # Success Case (Chance 55%, so < 0.55 passes)
        # Sequence:
        # 1. Dodge: 0.9 (Fail)
        # 2. Crit: 0.9 (Fail)
        # 3. Effect Condition (0.55): 0.5 (Pass)
        # 4. Potency Check: 0.1 (Pass)
        
        mock_random.side_effect = [0.9, 0.9, 0.5, 0.1]
        
        move = self.jkg.moves[0]
        self.jkg.complete_turn(self.game, selected_move=move)
        
        self.assertTrue(self.enemy.has_debuff(debuffs.Offense_Down), "Should apply Offense Down")
        
        # Reset
        self.enemy.debuffs = []
        
        # Failure Case (Chance 0.55, so > 0.55 fails)
        # Sequence: Dodge, Crit, Condition (0.6 -> Fail)
        mock_random.side_effect = [0.9, 0.9, 0.6]
        
        self.jkg.complete_turn(self.game, selected_move=move)
        self.assertFalse(self.enemy.has_debuff(debuffs.Offense_Down), "Should fail to apply Offense Down")

    @patch('main.Game.choose_targets')
    @patch('units.random.random')
    def test_saber_throw(self, mock_random, mock_targets):
        """
        Test Saber Throw (Special)
        Spec Check:
        - Deal Physical damage to all enemies.
        - 55% chance to inflict Ability Block for 1 turn.
        - Gain Defense Up for 2 turns.
        """
        mock_targets.return_value = self.enemy
        
        # Sequence:
        # 1. Dodge: 0.9
        # 2. Crit: 0.9
        # 3. Effect 1 (Abi Block) Condition (0.55): 0.1 (Pass)
        # 4. Effect 1 Potency: 0.1 (Pass)
        # 5. Effect 2 (Def Up): (No chance check, automatic on cast phase 'after_ability')
        
        mock_random.side_effect = [0.9, 0.9, 0.1, 0.1]
        
        move = self.jkg.moves[1]
        self.jkg.complete_turn(self.game, selected_move=move)
        
        self.assertTrue(self.enemy.has_debuff(debuffs.Ability_Block), "Should apply Ability Block")
        self.assertTrue(self.jkg.has_buff(buffs.Defense_Up), "Should gain Defense Up")

    def test_defend_the_order_stats(self):
        """
        Test Defend the Order (Unique) - Stat Bonus
        Spec Check:
        - While below 50% Health, have +30% Tenacity.
        """
        base_tenacity = self.jkg.tenacity
        
        # 1. Reduce Health below 50%
        # We need to trigger `on_damage_taken` manually or via damage mechanism to update the unique.
        # Direct assignment won't trigger `on_damage_taken`.
        # But `on_before_attacked` triggers checks too.
        # Let's verify `on_damage_taken` logic by simulating damage.
        
        damage_amount = self.jkg.max_health * 0.6
        # Apply damage manually via `apply_damage` is complex.
        # Let's use `health` setting then force a check?
        # The unique hooked `on_damage_taken`. 
        # But for test, we can just call `game.trigger_event("on_damage_taken", ...)`?
        # Or better, just set health and call a method that triggers it or wait for turn.
        
        self.jkg.health = self.jkg.max_health * 0.2
        
        # Call the unique logic helper directly? No, assume simulation.
        # Triggering `on_turn_start` should update it.
        self.jkg.on_turn_start(self.game)
        
        self.assertAlmostEqual(self.jkg.tenacity, base_tenacity + 0.30, delta=0.01, msg="Should have +30% Tenacity below 50% HP")
        
        # 2. Heal Above 50%
        self.jkg.health = self.jkg.max_health * 0.9
        self.jkg.on_turn_start(self.game) # Should remove it
        
        self.assertAlmostEqual(self.jkg.tenacity, base_tenacity, delta=0.01, msg="Should remove Tenacity bonus above 50% HP")

    def test_defend_the_order_heal(self):
        """
        Test Defend the Order (Unique) - Healing
        Spec Check:
        - Recover 15% Max Health at start of turn if below 50% Health.
        """
        # Set Health below 50%
        start_hp = int(self.jkg.max_health * 0.4)
        self.jkg.health = start_hp
        
        # Trigger turn start
        self.jkg.on_turn_start(self.game)
        
        expected_heal = round(self.jkg.max_health * 0.15)
        expected_hp = start_hp + expected_heal
        
        self.assertAlmostEqual(self.jkg.health, expected_hp, delta=5, msg="Should recover 15% Max Health")
        
        # Test Not Healing if above 50%
        self.jkg.health = int(self.jkg.max_health * 0.6)
        start_hp = self.jkg.health
        
        self.jkg.on_turn_start(self.game)
        
        self.assertEqual(self.jkg.health, start_hp, "Should not heal if above 50% HP")

if __name__ == '__main__':
    unittest.main()
