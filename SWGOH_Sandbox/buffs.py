class Buff:
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
        return Buff(
            kind     = self.kind,
            duration = duration,
            cant_be  = self.cant_be
        )

Accuracy_Up            = Buff("accuracy up", cant_be=["stackable"]) # +15% Accuracy
Advantage              = Buff("advantage", cant_be=["stackable"]) # Next attack will be a critical hit (if possible).
Afterburner            = Buff("afterburner", cant_be=[]) # When the TIE Silencer attacks with Advantage, reduce its cooldowns by 1. When a First Order ally takes damage, the TIE Silencer has a 50% chance to gain Advantage for 2 turns.
Backup_Plan            = Buff("backup plan", cant_be=["dispellable", "prevented"]) # Recover 10% Health per turn, Revive with 80% Health and 30% Turn Meter when defeated. Can't be Dispelled or prevented.
Baktoid_Shield_Generator = Buff("baktoid shield generator", cant_be=[]) # At the start of turn, recover 30% Protection and dispel own debuffs; Tanks Taunt while they have Protection.
Beskar_Armor           = Buff("beskar armor", cant_be=[]) # 1 Stack: +50% Defense and +15% Health Up. 2 Stacks: Recover 30% Protection at the end of turn. 3 Stacks: 100% Counter Chance and can't be critically hit.
BlasTech_Weapon_Mod    = Buff("blastech weapon mod", cant_be=[]) # Gain 15% Turn Meter at the start of each enemy's turn; Enemies defeated by this character can't be revived.
Bonus_Protection       = Buff("bonus protection", cant_be=[]) # Adds a variable amount of bonus protection for the rest of the battle.
Bounty_Hunters_Resolve = Buff("bounty hunter's resolve", cant_be=["dispellable", "prevented"]) # Ignores taunt and revives with 100% health when defeated. Can’t be Dispelled or prevented.
Breach_Immunity        = Buff("breach immunity", cant_be=["stackable"]) # Can't apply Breach to this unit.
Call_to_Action         = Buff("call to action", cant_be=["dispellable", "prevented"]) # Luke ignores Taunts during his turn and has +50% Accuracy, +50% Critical Chance, and + 50% Critical Damage. Can't be Dispelled or prevented.
Chaff                  = Buff("chaff", cant_be=["stackable"]) # Immune to target lock
Chiewab_Medpac         = Buff("chiewab medpac", cant_be=[]) # Recover 5% Health and Protection at the start of every character's turn, and 5% bonus Protection if this character is a Separatist.
Critical_Avoidance_Up  = Buff("critical avoidance up", cant_be=["stackable"]) # +50% Critical Avoidance
Critical_Chance_Up     = Buff("critical chance up", cant_be=["stackable"]) # +25% Critical Chance
Critical_Damage_Up     = Buff("critical damage up", cant_be=["stackable"]) # +50% Critical Damage
Critical_Hit_Immunity  = Buff("critical hit immunity", cant_be=["stackable"]) # Can't be critically hit.
Damage_Immunity        = Buff("damage immunity", cant_be=["stackable", "copyable"]) # Prevents all damage.
Dark_Infusion          = Buff("dark infusion", cant_be=[]) # +35% Offense per stack (max 3 stacks). At max stacks, these bonuses are doubled and Basic attacks also inflict Healing Immunity for 2 turns.
Deep_Cover             = Buff("deep cover", cant_be=[]) # +10% Defense Penetration and Potency per stack
Defense_Penetration_Up = Buff("defense penetration up", cant_be=["stackable"]) # +150 Defense Penetration
Defense_Up             = Buff("defense up", cant_be=["stackable"]) # +50% Defense
Deflector_Shield       = Buff("deflector shield", cant_be=["copyable"]) # At start of turn, recover 25% Protection, doubled for Resistance allies, and gain Foresight for 2 turns; can't be copied
Dramatic_Entrance      = Buff("dramatic entrance", cant_be=[]) # +25% Offense and deal bonus damage equal to 10% of the targets max health. Gain 20% Turn Meter and regain Dramatic Entrance for 2 turns after defeating an enemy while this buff is active.
Evasion_Up             = Buff("evasion up", cant_be=["stackable"]) # +15% Dodge Chance
Force_Connection       = Buff("force connection", cant_be=[]) # +2% Defense and Offense per stack
Foresight              = Buff("foresight", cant_be=["stackable"]) # Evades the next attack (if able).
Formation              = Buff("formation", cant_be=[]) # +10% Max Health, Offense, and Potency; whenever this ship uses an ability, gain 1% Turn Meter per stack of Formation
Frenzy                 = Buff("frenzy", cant_be=["stackable"]) # Gain 100% Turn Meter when an ally uses a Special ability.
Hatred                 = Buff("hatred", cant_be=[]) # Increases offense and defense by 100% and crit chance by 25%. When this unit is defeated, they revive with 100% Health, and gain 100% Turn Meter.
Heal_Over_Time         = Buff("heal over time", cant_be=[]) # Heals a variable amount each turn.
Health_Steal_Up        = Buff("health steal up", cant_be=["stackable"]) # +50% Health Steal
Health_Up              = Buff("health up", cant_be=["stackable"]) # +15% Max Health
High_Ground            = Buff("high ground", cant_be=[]) # Deals 35% more damage with out of turn attacks; +100% Counter Chance; -35% Speed; can't gain Ultimate Charge
Hired_Muscle           = Buff("hired muscle", cant_be=["stackable"]) # +30% Tenacity; immune to Daze and Fear
Jedi_Knight            = Buff("jedi knight", cant_be=[]) # Kyle Katarn and Rebel Fighter allies gain 50% Defense and Offense; can't gain Force Connection.
Jedi_Legacy            = Buff("jedi legacy", cant_be=[]) # +100% Mastery and ignores Taunt during their turn; can't gain Jedi Lessons
Jedi_Lessons           = Buff("jedi lessons", cant_be=[]) # +20% Mastery per stack (max 3 stacks).
Jedis_Will             = Buff("jedi's will", cant_be=[]) # +100% Counter Chance, +25% Offense, and +25% Speed
Legendary_Battle_Meditation = Buff("legendary battle meditation", cant_be=["stackable"]) # +25%-50% Potency and +10%-35% Counter Chance, doubled for Jedi.
Lifeblood              = Buff("lifeblood", cant_be=[]) # Damage received decreased by 30% and damage dealt increased by 30%.
Loyal_Hand             = Buff("loyal hand", cant_be=[]) # +10% Max Protection and Offense (stacking, max 20)
Mandalor               = Buff("mand'alor", cant_be=[]) # Mandalorian allies assist dealing 50% less damage when this character uses an ability during their turn; at the start of every turn, dispel all debuffs on the healthiest Mandalorian ally without Mand'alor and that ally gains Taunt and +100% Defense until the end of that turn; defeating this character will grant Mand'alor to the character that defeated them; if this character is defeated by a  Mand'alor will not be granted to anyone
Master_Plan            = Buff("master plan", cant_be=[]) # After this ship uses an ability during its turn, their cooldowns are reset and they gain 100% Turn Meter.
Masters_Training       = Buff("master's training", cant_be=["dispellable", "prevented"]) # +25% (doubled on Jedi) Accuracy, Defense, Offense, Potency, and Tenacity. Can't be Dispelled or Prevented.
Mechanics_Savvy        = Buff("mechanic's savvy", cant_be=["stackable"]) # Droids: +40% Offense;When defeated, revive with 80% Health and Protection. Scoundrels: +20% Critical Chance, +40% Critical Damage and Defense Penetration
Merciless              = Buff("merciless", cant_be=["stackable"]) # +50% Offense, +25% Critical Chance, and +50% Critical Damage; immune to Fear and Turn Meter manipulation.
My_Kind_of_Scum        = Buff("my kind of scum", cant_be=[]) # +10% Max Health and Defense per stack
Offense_Up             = Buff("offense up", cant_be=["stackable"]) # +50% Offense
Outmaneuver            = Buff("outmaneuver", cant_be=["stackable"]) # +25% Evasion and can’t be countered, and can't be targeted if other allies are present, unless Taunting.
Overcharge             = Buff("overcharge", cant_be=["copyable"]) # +20% Offense and Defense per stack (max 5 stacks), can't be copied
Pilots_Resolve         = Buff("pilot's resolve", cant_be=[]) # The first time Razor Crest is reduced to 1% Health, it recovers 90% Health and gains 3 stacks of Reinforced Hull.
Potency_Up             = Buff("potency up", cant_be=["stackable"]) # +50% Potency
Protection_Over_Time   = Buff("protection over time", cant_be=[]) # Heals a variable amount of Protection each turn for a specified number of turns.
Protection_Up          = Buff("protection up", cant_be=[]) # Increases Protection by specified amount of max health for specified number of turns.
Ransom                 = Buff("ransom", cant_be=[]) # +2% Max Health and Tenacity per stack
Reinforced_Determination = Buff("reinforced determination", cant_be=["stackable"]) # +50% Defense per stack
Reinforced_Hull        = Buff("reinforced hull", cant_be=[]) # +250% Defense per stack; lose one stack of Reinforced Hull when receiving damage
Resilient_Defense      = Buff("resilient defense", cant_be=["stackable"]) # Enemies will target this unit; lose one stack when damaged by an attack.
Retaliate              = Buff("retaliate", cant_be=["stackable"]) # Enemies will target this unit.
Retribution            = Buff("retribution", cant_be=["stackable"]) # Adds 100% counter chance.
Riposte                = Buff("riposte", cant_be=["copyable", "stackable"]) # Attacks out of turn ignore Protection, can't be copied
Ruthless               = Buff("ruthless", cant_be=[]) # +15% Critical Chance, +20% Critical Damage, and +30% Offense
Secret_Intel           = Buff("secret intel", cant_be=["stackable"]) # +25% Potency and when another ally uses a Special ability they gain Secret Intel for 3 turns, then the cooldown of Illuminated Destiny is reduced by 1 for each ally with Secret Intel.
Shien                  = Buff("shien", cant_be=[]) # Whenever this unit evades, or attacks out of turn, Commander Ahsoka Tano's Force Leap cooldown is reduced by 1 and damage is increased by 50% (stacking) until the next time it is used
Spare_Parts            = Buff("spare parts", cant_be=[]) # +30% Critical Chance and +30% Offense, if this character is defeated, they are revived with 100% Health, gain Foresight and Protection Up (50%) for 2 turns, and dispel the buff from all allies, this revive can't be prevented.
Spark_of_Rebellion     = Buff("spark of rebellion", cant_be=["stackable"]) # Gain 40% Offense and 30 Speed; when this character attacks, recover 20% Max Health and Protection; Empire enemies defeated by this character can't be revived; if Spark of Rebellion is dispelled, gain 40% Turn Meter, 5% Upload progress, and Protection Up (50%) for 2 turns.
Speed_Up               = Buff("speed up", cant_be=["stackable"]) # +25% Speed
Stable_Bulwark         = Buff("stable bulwark", cant_be=[]) # +100% Defense and Offense; +50% Max Health and Max Protection, +25% Critical Chance and Critical Damage; the first time this ship is reduced to 1% Health, it recovers 100% Health, gains a bonus turn, gains 5 stacks of Reinforced Determination for 1 turn, and loses Stable Bulwark
Stealth                = Buff("stealth", cant_be=["stackable"]) # Character cannot be targeted directly.
Suprosa_Supercomputer  = Buff("suprosa supercomputer", cant_be=[]) # Gain 100% Critical Chance and an additional bonus based on the ship's role. Attacker: At the start of turn, dispel Stealth and Taunt from all enemies and inflict Defense Down for 1 turn on a random enemy. Tank: All Rebel allies recover 10% Health and Protection whenever this ship receives damage. Support: At the start of turn, inflict Target Lock on a random enemy for 2 turns and remove 20% Turn Meter
Tactical_Genius        = Buff("tactical genius", cant_be=["stackable"]) # First ally with this buff to use a Special ability heals and gains 100% Turn Meter.
Tactical_Supremacy     = Buff("tactical supremacy", cant_be=["stackable"]) # +30% Critical Damage and Potency; recover 10% Protection at the start of turn; if dispelled, recover 40% Health then gain Advantage and Foresight for 2 turns at the end of that turn
Target_Practice        = Buff("target practice", cant_be=[]) # +5% Critical Chance, +5% Offense, and +10% Critical Damage per stack
Taunt                  = Buff("taunt", cant_be=["stackable", "copyable"]) # Enemies will target this unit.
Tenacity_Up            = Buff("tenacity up", cant_be=["stackable"]) # Resist negative .
The_Emperors_Trap      = Buff("the emperor's trap", cant_be=[]) # +6% Offense and Potency per stack
Thrust_Reversal        = Buff("thrust reversal", cant_be=[]) # +100% counter chance, Whenever the Falcon uses its basic attack, 1 stack is consumed to gain 50% Turn Meter.
Translation            = Buff("translation", cant_be=["stackable"]) # 1 Stack: +30% Max Health. 2 Stacks: 15% Critical Chance. 3 Stacks: If only one ally who grants Translation is present, decrease this character's cooldowns by 1 when that ally uses their Basic ability (limit once per turn)
Trusted_Agent          = Buff("trusted agent", cant_be=[]) # +30% Defense Penetration and Offense; at 1 or more stacks, attack again when performing a Basic attack
Unending_Loyalty       = Buff("unending loyalty", cant_be=[]) # Can't be defeated during the first enemy attack (including assists) that would otherwise defeat this ship. When reduced to 1% Health, gain Stealth and Protection Up (50%) for 2 turns and recover 25% Health. Then, this buff expires.
Valor                  = Buff("valor", cant_be=["stackable"]) # Grant allied Galactic Republic Capital Ship 15% Turn Meter and reduce its ultimate ability's cooldown by 1 at end of turn.
We_Adapt_Or_Die        = Buff("we adapt, or die", cant_be=["stackable"]) # +30% Critical Chance, +30% Offense, and +30 Speed; revive with 70% Health when defeated; if dispelled, recover 80% Health, gain 80% Turn Meter, and can't be critically hit for 2 turns
We_Dont_Need_Their_Scum= Buff("we don't need their scum", cant_be=[]) # Immune to Turn Meter manipulation; whenever a Bounty Hunter ally is defeated, recover 25% Health and Protection; TIE Advanced x1 instead recovers 10% Health and Protection
We_Have_Returned       = Buff("we have returned", cant_be=[]) # +5% Critical Damage and Offense per stack