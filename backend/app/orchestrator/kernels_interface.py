from app.orchestrator.kernels import (
    CortexKernel,
    EmpireKernel,
    GenesisKernel,
    HiveKernel,
    RPGKernel,
    SocietyKernel,
)


class KernelInterface:
    """
    Central interface for accessing all simulation kernels.
    Ensures single instances of kernels are shared across the orchestrator.
    """
    def __init__(self):
        self.genesis = GenesisKernel()
        self.empire = EmpireKernel()
        self.hive = HiveKernel()
        self.society = SocietyKernel()
        self.cortex = CortexKernel()
        self.rpg = RPGKernel()
