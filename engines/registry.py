# engines/registry.py

from engines.rot import StaticRot, AlbertiRot, VigenereRot
from engines.plugboard import PlugboardEngine

ENGINE_REGISTRY = {
    "static_rot": lambda cfg, alpha: StaticRot(alpha, cfg["shift"]),
    "alberti_rot": lambda cfg, alpha: AlbertiRot(alpha, cfg["initial_shift"], cfg["shift_interval"], cfg["shift_step"]),
    "vigenere_rot": lambda cfg, alpha: VigenereRot(alpha, cfg["key_stream"]),
    "plugboard": lambda cfg, _: PlugboardEngine(cfg["map"]),
}

