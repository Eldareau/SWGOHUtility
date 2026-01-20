class Debuff:
    def __init__(self, kind, duration=0, cant_be=None):
        self.kind     = kind
        self.duration = duration
        self.cant_be  = cant_be if cant_be is not None else []

    def __repr__(self):
        return f"{self.kind} ({self.duration})"
    
    def __eq__(self, value):
        return self.kind == value.kind and self.cant_be == value.cant_be
    
    def copy(self, duration):
        """Create a safe copy, optionally overriding duration."""
        return Debuff(
            kind     = self.kind,
            duration = duration,
            cant_be  = self.cant_be
        )

Ability_Block          = Debuff("ability block", cant_be=["stackable"]) #Special abilities are unusable
Accuracy_Down          = Debuff("accuracy down", cant_be=["stackable"]) # -15% Accuracy
Anguish                = Debuff("anguish", cant_be=[]) # Takes damage at the start of their turn equal to 2% of their Max Health for each stack of Anguish and gains that much Offense until the end of their turn; this character can't be defeated by this damage
Blind                  = Debuff("blind", cant_be=["stackable"]) # Miss the next attack.
Breach                 = Debuff("breach", cant_be=["stackable"]) # -25% Speed, -25% Defense (Does not stack with Speed Down or Defense Down)
Buff_Immunity          = Debuff("buff immunity", cant_be=["stackable"]) # Immune to buffs.
Burning                = Debuff("burning", cant_be=["stackable"]) # -15% (0.03% for raid bosses) of max health per turn, reduces avoidance by 500000%; does not stack.
Buzz_Droids            = Debuff("buzz droids", cant_be=[]) # -50% Defense and lose 5% Health at start of turn with at least 1 Buzz Droid (max 3); lose 1 Buzz Droid when taking damage from an attack or a Concussion Mine.
Captive                = Debuff("captive", cant_be=["stackable"]) # Speed set to 0, can't bonus attack or gain bonus Turn Meter
Concussion_Mine        = Debuff("concussion mine", cant_be=["dispellable", "stackable"]) # Deals damage equal to 10% of targets max health and Dazes the target for 2 turns when it explodes. Can't be dispelled.
Confuse                = Debuff("confuse", cant_be=[]) # 1 Stack: Cannot gain buffs. 2 Stacks: Cannot counter, assist, or gain bonus turn meter. (Raid Boss: -30% Counter chance.) 3 Stacks: Increases cooldowns by 1 when this character uses their basic ability. (Raid Boss: -50% Defense.)
Corrupted_Battle_Meditation = Debuff("corrupted battle meditation", cant_be=["dispellable", "stackable"]) # -10%-30% Crit Chance and -10%-30% Counter Chance. Doubled against non-Sith and non-Jedi enemies. Can't be dispelled.
Critical_Chance_Down   = Debuff("critical chance down", cant_be=["stackable"]) # Removes 25% critical chance.
Critical_Damage_Down   = Debuff("critical damage down", cant_be=["stackable"]) # -50% Critical Damage
Damage_Over_Time       = Debuff("damage over time", cant_be=[]) # Character loses 5% (0.01% for raid bosses) of max health each turn.
Daze                   = Debuff("daze", cant_be=["stackable"]) # Can't assist, counter attack, or gain bonus Turn Meter
Deathmark              = Debuff("deathmark", cant_be=["stackable"]) # Enemies will target this unit, -50% Health if damaged by attack (0.03% for raid bosses), can't revive.
Deceived               = Debuff("deceived", cant_be=["stackable"]) # Can't target Sith Eternal Emperor during their turn if another Sith enemy is active. When an ability is used, Sith Eternal Emperor gain's 2% Ultimate Charge and recover's 2% Protection. Can't counter attack.
Defense_Down           = Debuff("defense down", cant_be=["stackable"]) # Decreases defense by 50%.
Defense_Penetration_Down = Debuff("defense penetration down", cant_be=["stackable"]) # -150 Defense Penetration
Demoralized            = Debuff("demoralized", cant_be=["stackable"]) # -50% Offense, -25% Critical Chance, -25% Critical Damage; does not stack with other debuffs
Disarm                 = Debuff("disarm", cant_be=["stackable"]) # -50% Critical Damage and Offense (doesn't stack with Critical Damage Down or Offense Down); whenever this character uses a Basic ability, they gain Damage Over Time for 2 turns, which can't be resisted
Doubt                  = Debuff("doubt", cant_be=["stackable"]) # Can't gain bonus Turn Meter or buffs or recover Protection
Evasion_Down           = Debuff("evasion down", cant_be=["stackable"]) # Removes 25% dodge chance.
Expose                 = Debuff("expose", cant_be=["stackable"]) # -20% (0.02% for raid bosses) of max health if damaged by attack.
Fear                   = Debuff("fear", cant_be=["stackable"]) # Miss the next turn, can't use abilities, and can't evade. Increase cooldowns by 1 and Fear expires on taking damage from an attack.
Ferocity               = Debuff("ferocity", cant_be=["copyable"]) # -15% Defense and Tenacity per stack, +8% Offense and Potency per stack; cant' be copied.
Force_Influence        = Debuff("force influence", cant_be=["stackable"]) # Can't assist, counter attack or gain buffs (raid bosses and Galactic Legends: -30% counter chance)
Fracture               = Debuff("fracture", cant_be=["stackable"]) # Speed set to 0, cannot gain buffs, bonus attacks, or turn meter. Raid bosses lose 0% speed, 30% counter chance, and cannot gain buffs.
Healing_Immunity       = Debuff("healing immunity", cant_be=["stackable"]) # Character cannot regain health or protection.
Health_Down            = Debuff("health down", cant_be=["stackable"]) # Decreases health by 20%.
Health_Steal_Down      = Debuff("health steal down", cant_be=["stackable"]) # Decreases health steal by 50%.
Hunted                 = Debuff("hunted", cant_be=["stackable"]) # Deals 75% less damage with out of turn attacks and can't gain bonus Turn Meter.
Inevitable_Failure     = Debuff("inevitable failure", cant_be=[]) # Gain 1 stack when using an ability or receiving damage from an enemy; when defeated, grant Admiral Piett bonuses based on the number of stacks this unit until the end of battle.
Marked                 = Debuff("marked", cant_be=["stackable", "copyable"]) # Enemies will target this unit.
Offense_Down           = Debuff("offense down", cant_be=["stackable"]) # -50% Offense.
Overconfident          = Debuff("overconfident", cant_be=["stackable"]) # -20% Defense, +50% Offense, +10% Speed, +15% Evasion
Pain                   = Debuff("pain", cant_be=["stackable"]) # Take bonus damage equal to 10% (0.05% for raid bosses) of Max Health when damaged by Darth Sion.
Pinned                 = Debuff("pinned", cant_be=["stackable"]) # Can't gain bonus Turn Meter and has -25% Speed, doesn't stack with Breach or Speed Down
Plague                 = Debuff("plague", cant_be=["dispellable"]) # Lose 5% (0.01% for raid bosses) Health, per stack, when inflicted and at the start of their turn, is immune to allied Dispels, and loses all stacks of Plague when healed to full Health. This damage ignores protection.
Potency_Down           = Debuff("potency down", cant_be=["stackable"]) # Decreased chance to apply detrimental effects. -50% Potency.
Protection_Disruption  = Debuff("protection disruption", cant_be=["stackable"]) # Protection is disabled, immune to Protection Up and Bonus Protection.
Provoked               = Debuff("provoked", cant_be=["stackable"]) # +100% counter chance; this character deals 90% less damage when attacking out of turn; whenever this character attacks out of turn, they take damage equal to 20% of their Max Health; this damage can't defeat this character
Purge                  = Debuff("purge", cant_be=["copyable", "prevented"]) # Increased effects from enemies that utilize Purge which lasts until the end of the encounter and can't be copied or prevented.
Shatterpoint           = Debuff("shatterpoint", cant_be=["stackable"]) # Receiving damage dispels Shatterpoint and reduces Defense, Max Health, and Offense by 10% for the rest of the encounter; enemies can ignore Taunt to target this unit.
Shield_Disruption      = Debuff("shield disruption", cant_be=["stackable"]) # Protection is disabled, immune to Protection Up and Bonus Protection.
Shock                  = Debuff("shock", cant_be=["stackable"]) # Character cannot heal, gain buffs, or gain bonus turn meter.
Speed_Down             = Debuff("speed down", cant_be=["stackable"]) # -25% Speed.
Stagger                = Debuff("stagger", cant_be=["stackable"]) # Lost 100% Turn Meter if damaged by attack.
Stranded               = Debuff("stranded", cant_be=["stackable"]) # Take damage equal to 35% of its Max Health at start of its turn; this damage can't defeat a unit; can't recover Health or Protection, or gain Protection Up
Stun                   = Debuff("stun", cant_be=["stackable"]) # Character misses a turn and cannot avoid attacks.
Suspense               = Debuff("suspense", cant_be=["stackable"]) # Can't gain buffs; Gaining bonus Turn Meter, recovering Protection, or gaining Protection Up will inflict Defense Down for 2 turns, which can't be evaded or resisted; if Suspense is dispelled, increase cooldowns by 1, which can't be resisted; If Suspense expires and is not dispelled, all Sith and Sith Empire enemies gain a stack of We Have Returned for 4 turns, which can't be copied, dispelled, or prevented
Target_Lock            = Debuff("target lock", cant_be=["stackable"]) # Increased effects from abilities that utilize Target Lock. Interacts with units ability mechanics
Tenacity_Down          = Debuff("tenacity down", cant_be=["stackable"]) # Minimized chance to resist negative status effects.
Torture                = Debuff("torture", cant_be=["stackable"]) # Take bonus damage equal to 10% of this character's Max Health when damaged by an attack; reduce Defense by 10% (stacking, max 50%) for the rest of the encounter when damaged by an attack; can't gain bonus Turn Meter
Useful_Pawn            = Debuff("useful pawn", cant_be=["stackable"]) # -5% Critical Chance, Critical Damage, and Offense
Vulnerable             = Debuff("vulnerable", cant_be=["stackable"]) # Will be critically hit if able.