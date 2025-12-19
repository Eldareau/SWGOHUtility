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
    
Ability_Block    = Debuff("ability block", cant_be=["stackable"])
Buff_Immunity    = Debuff("buff immunity", cant_be=["stackable"])
Daze             = Debuff("daze", cant_be=["stackable"]) #todo: Can't gain bonus Turn Meter
Defense_Down     = Debuff("defense down", cant_be=["stackable"])
Healing_Immunity = Debuff("healing immunity", cant_be=["stackable"])
Marked           = Debuff("marked", cant_be=["stackable", "copyable"])
Stun             = Debuff("stun", cant_be=["stackable"])
Target_Lock      = Debuff("Target_Lock", cant_be=["stackable"])
Vulnerable       = Debuff("vulnerable", cant_be=["stackable"])