class Other:
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
        return Other(
            kind     = self.kind,
            duration = duration,
            cant_be  = self.cant_be
        )

Armor_Shred            = Other("armor shred", -1, cant_be=["dispellable", "copyable"]) # -50% Defense per stack (25% against raid bosses), can't be dispelled or resisted, and is not a debuff.
Advance                = Other("advance", -1, cant_be=["dispellable", "prevented", "copyable", "stackable"]) # Taunt,which can't be dispelled or prevented. Other 501st allies can't lose Health.
Ashes_of_the_Republic  = Other("ashes of the republic", -1, cant_be=["dispellable", "prevented"]) # Lord Vader's abilities gain additional effects; enemies defeated while this is active can't be revived; Lord Vader is immune to Ability Block, Healing Immunity, and Shock; can't gain Ultimate Charge
Beskar_Ingot           = Other("beskar ingot", -1, cant_be=["stackable"]) # Used to bestow Beskar Armor on allies. Max 3 stacks.
Capital_Ship_Sabotaged = Other("capital ship sabotaged", -1, cant_be=["dispellable", "prevented"]) # The next allied ship called to Reinforce is immediately destroyed upon deployment
Charge                 = Other("charge", -1, cant_be=["dispellable", "prevented"]) # +5% Offense per stack
Command                = Other("command", -1, cant_be=["dispellable", "prevented"]) # The Blaster Turret assists whenever this character uses an ability during their turn
Contract               = Other("contract", -1, cant_be=["dispellable", "prevented"]) # Varies based on lead bounty hunter contract
Courage                = Other("courage", -1, cant_be=["dispellable", "prevented"]) # When damaging the target enemy with an ability, for each 5 stacks of Courage, dispel 5 stacks and deal bonus damage equal to 40% of the target's Max Health.
Cover                  = Other("cover", -1, cant_be=["dispellable", "prevented", "copyable", "stackable"]) # Can't be targeted, immune to damage and status effects, speed set to 0, recover 10% Protection and Turn Meter at the end of every turn, which can't be prevented.
Dark_Trooper_Squad     = Other("dark trooper squad", -1, cant_be=["dispellable", "prevented"]) # This unit has 25% of its base Max Health and Max Protection, is immune to Max Health and Max Protection changes and can't be defeated or destroyed while it has more than one stack of Dark Trooper Squad.
Deadly_Bluff           = Other("deadly bluff", -1, cant_be=["dispellable", "prevented"]) # Boushh's Abilities gain additional effects against this character
Determination          = Other("determination", -1, cant_be=["dispellable", "prevented"]) # Whenever any other Resistance ally falls below 50% Health, Determination expires and Finn Taunts for 2 turns. If that ally was Taunting, it is dispelled. When Determination expires, Finn gains Retribution for 2 turns.
Devouring_Swarm        = Other("devouring swarm", -1, cant_be=["dispellable", "prevented"]) # +2% Offense per stack
Dominance              = Other("dominance", -1, cant_be=["dispellable", "prevented"]) # Enemies can't counterattack;First Order allies have +100% counter chance and +50% Critical Damage
Droid_Battalion        = Other("droid battalion", -1, cant_be=["dispellable", "prevented"]) # Each stack grants B1 +2% Offense and all Separatist allies +0.5% Tenacity and Critical Avoidance.
Endless_Horde          = Other("endless horde", -1, cant_be=["dispellable", "prevented"]) # If Nightsister Zombie survived damage from her last turn, she gains 50% Speed (stacking) at the start of her turn. When Nightsister Zombie is defeated, she loses 50% Speed (stacking). The effects are neither buffs nor debuffs and combine for a maximum of +100% Speed or a minimum of -100% Speed. If Nightsister Zombie is defeated while at -100% Speed from this effect, she cannot be revived.
Extortion              = Other("extortion", -1, cant_be=["dispellable", "prevented"]) # Using Extortion removes it, recover 10% Health, and grants Separatist enemies Profit.
Force_Energy           = Other("force energy", -1, cant_be=["dispellable", "prevented"]) # At 100 stacks, lose all stacks and gain Unleashed
Furious                = Other("furious", -1, cant_be=["dispellable", "prevented"]) # Abilities gain additional effects, can't gain Fury
Fury                   = Other("fury", -1, cant_be=["dispellable", "prevented"]) # At 10 stacks, is consumed and character gains Furious instead.
Guard                  = Other("guard", -1, cant_be=["dispellable", "prevented"]) # Can't be critically hit, immune to Daze and Stun, +25% Critical Chance
Hive_Mind              = Other("hive mind", -1, cant_be=["dispellable", "prevented"]) # Various effects depending on character and ability. Cannot be dispelled or prevented.
Insight                = Other("insight", -1, cant_be=["dispellable", "prevented"]) # Characters gain additional effects and abilities based on the number of stacks.
Inspired               = Other("inspired", -1, cant_be=["dispellable", "prevented"]) # Resistance characters gain bonuses when they are Inspired; this effect expires after receiving 3 critical hits
Isolate                = Other("isolate", -1, cant_be=["dispellable", "prevented", "copyable"]) # Can’t attack, gain buffs, or gain other positive effects during another characters turn. Allies can’t attack or gain buffs during this characters turn. Raid bosses cannot gain buffs, and any allies who damage the boss gain Crit Damage Up and Health Steal Up for 1 turn. Can’t be copied or dispelled.
Leader_Contract_Reward = Other("leader contract reward", -1, cant_be=["dispellable", "prevented"]) # Various effects depending on the squad leader. Cannot be dispelled or prevented.
Linked                 = Other("linked", -1, cant_be=["dispellable", "prevented"]) # This character is Linked. At the start of a Linked characters turn each Linked enemy loses 20% Max Protection and Sith Eternal Emperor gains 25% of the amount lost. Cannot critically hit and damage dealt is decreased by 25%.
Mastery_Decreased      = Other("mastery decreased", -1, cant_be=["dispellable", "prevented"]) # This unit's current Mastery is lower than its starting value.
Mastery_Increased      = Other("mastery increased", -1, cant_be=["dispellable", "prevented"]) # This unit's current Mastery is higher than its starting value.
Merciless_Target       = Other("merciless target", -1, cant_be=["dispellable", "prevented"]) # Darth Vader must target a unit with this or a taunt effect and takes a bonus turn after using an ability while targeting this unit. This effect cannot be evaded or resisted.
MK_I                   = Other("mk i", -1, cant_be=["dispellable", "prevented"]) # Gain +50% Counter Chance for the rest of the battle and become Prepared. When used, this ability upgrades to MK II
MK_II                  = Other("mk ii", -1, cant_be=["dispellable", "prevented"]) # Gain +30% Critical Avoidance and +1--% Defense for the rest of the battle and become Prepared. When used, this ability upgrades to MK III
MK_III                 = Other("mk iii", -1, cant_be=["dispellable", "prevented"]) # Increase Counter Chance to 100% for the rest of the battle and become Prepared. This ability may only be used once.
Momentum               = Other("momentum", -1, cant_be=["dispellable", "prevented"]) # Abilities gain additional effects based on the number of stacks.
Operation_Knightfall   = Other("operation knightfall", -1, cant_be=["dispellable", "prevented"]) # When Knightfall Trooper is defeated, remove 1 stack of Operation Knightfall from Appo and summon a Knightfall Trooper
Padawan_Lessons        = Other("padawan lessons", -1, cant_be=["dispellable", "prevented"]) # kelleran-beq
Payout                 = Other("payout", -1, cant_be=["dispellable", "prevented"]) # Various effects depending on the specific character. Cannot be dispelled or prevented.
Persistence            = Other("persistence", -1, cant_be=["dispellable", "prevented"]) # At the start of his turn, Cal does the following based on the number of stacks of Persistence that he has: - 10+ stacks: He and all Unaligned Force User allies gain Foresight for 2 turns - 20+ stacks: He and all Unaligned Force User allies gain Defense Up and Protection Up (30%) for 2 turns - 30 stacks: He inflicts Ability Block and Buff Immunity on all enemies for 2 turns, which can't be evaded or resisted, and all allies gain 50% Turn Meter, this effect is doubled for Light Side Unaligned Force Users; stacks of Persistence are reset
Plasma_Shielding       = Other("plasma shielding", -1, cant_be=["dispellable", "prevented"]) # While the Shield Generator has this, its allies gain bonuses
Prepared               = Other("prepared", -1, cant_be=["dispellable", "prevented"]) # Increased benefits from abilities that utilize the Prepared status. Cannot be dispelled or prevented.
Profit                 = Other("profit", -1, cant_be=["dispellable", "prevented"]) # +10% Critical Chance and Critical Damage per stack (max 50%) until the end of battle.
Purrgil_Migration      = Other("purrgil migration", -1, cant_be=["dispellable", "prevented"]) # +1% Defense and +1% Tenacity
Pursued_Target         = Other("pursued target", -1, cant_be=["dispellable", "prevented"]) # When TIE/IN interceptor Prototype targets this unit with an ability during its turn, it gains 40% Turn Meter; TIE/IN interceptor Prototype must target a unit with this or a taunt effect and can ignore taunt effects to target this unit
Recharge               = Other("recharge", -1, cant_be=["dispellable", "prevented"]) # This unit will take a bonus turn when all stacks expire
Ruse                   = Other("ruse", -1, cant_be=["dispellable", "prevented"]) # This effect triggers additional effects in abilities. Ruse is removed at the end of the turn.
Seasoned_Veteran       = Other("seasoned veteran", -1, cant_be=["dispellable", "prevented"]) # Fennec Shand can ignore Taunt and gains additional effects on her abilities
Siphon                 = Other("siphon", -1, cant_be=["dispellable", "prevented"]) # This unit will gain 1% of a stat per stack and the target will lose the amount gained.
Special_Forces         = Other("special forces", -1, cant_be=["dispellable", "prevented"]) # Gives abilities additional effects
Speed_Limitation       = Other("speed limitation", -1, cant_be=["dispellable", "prevented"]) # Speed 0, which can't be manipulated by other Speed limiting effects.
Strategic_Advantage    = Other("strategic advantage", -1, cant_be=["dispellable", "prevented"]) # Dispel all debuffs on target other Jedi ally. They gain Strategic Advantage and assist, using their Basic ability. This character uses their Basic ability and loses Strategic Advantage.
The_Sweet_Spot         = Other("the sweet spot", -1, cant_be=["dispellable", "prevented"]) # Increased effects from abilities that utilize The Sweet Spot
Thermal_Detonator      = Other("thermal detonator", 2, cant_be=["copyable"]) # Deals damage when timer expires. Character loses a variable amount of health after a specified number of turns.
Underestimated         = Other("underestimated", -1, cant_be=["dispellable", "prevented"]) # Gives abilities additional effects.
Unleashed              = Other("unleashed", -1, cant_be=["dispellable", "prevented"]) # Starkiller's abilities gain additional effects; can't gain Force Energy
Vengeance              = Other("vengeance", -1, cant_be=["dispellable", "prevented"]) # At 15 stacks, dispel all debuffs on all Sith allies, gain a bonus turn, then lose all stacks
VIP                    = Other("vip", -1, cant_be=["dispellable", "prevented"]) # When receiving damage, gain bonuses from characters that utilize VIP.
Whistling_Birds        = Other("whistling birds", -1, cant_be=["dispellable", "prevented"]) # Deal true damage to target enemy for each stack when using Swift Takedown, if target enemy is defeated by this, remaining Whistling Birds will damage the weakest remaining enemy.
Zeroed_In              = Other("zeroed in", -1, cant_be=["dispellable", "prevented"]) # Omega has Target Practice while a character is afflicted by this; Omega can ignore Taunt to target this enemy