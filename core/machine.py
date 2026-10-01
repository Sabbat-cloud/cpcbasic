class Z80Registers:
    def __init__(self):
        self.A = 0
        self.F = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.H = 0
        self.L = 0
        self.IX = 0
        self.IY = 0
        self.SP = 0xC000
        self.PC = 0

    @property
    def AF(self): return (self.A << 8) | self.F
    @AF.setter
    def AF(self, val): self.A = (val >> 8) & 0xFF; self.F = val & 0xFF

    @property
    def BC(self): return (self.B << 8) | self.C
    @BC.setter
    def BC(self, val): self.B = (val >> 8) & 0xFF; self.C = val & 0xFF

    @property
    def DE(self): return (self.D << 8) | self.E
    @DE.setter
    def DE(self, val): self.D = (val >> 8) & 0xFF; self.E = val & 0xFF

    @property
    def HL(self): return (self.H << 8) | self.L
    @HL.setter
    def HL(self, val): self.H = (val >> 8) & 0xFF; self.L = val & 0xFF
