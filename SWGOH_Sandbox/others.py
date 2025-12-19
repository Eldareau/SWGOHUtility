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
    
Armor_Shred = Other("armor shred", -1, cant_be=["dispellable", "copyable"])
Advance     = Other("advance", -1, cant_be=["dispellable", "prevented", "copyable", "stackable"])
Cover       = Other("cover", -1, cant_be=["dispellable", "prevented", "copyable", "stackable"])