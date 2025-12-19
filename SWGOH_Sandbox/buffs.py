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

Advantage             = Buff("advantage", cant_be=["stackable"])
Critical_Hit_Immunity = Buff("critical hit immunity", cant_be=["stackable"])
Damage_Immunity       = Buff("damage immunity", cant_be=["stackable", "copyable"])
Defense_Up            = Buff("defense up", cant_be=["stackable"])
Foresight             = Buff("foresight", cant_be=["stackable"])
Health_Steal_Up       = Buff("health steal up", cant_be=["stackable"])
Stealth               = Buff("stealth", cant_be=["stackable"])
Taunt                 = Buff("taunt", cant_be=["stackable", "copyable"])