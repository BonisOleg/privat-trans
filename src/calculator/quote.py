"""Mock freight quote. Not a real tariff engine."""

from dataclasses import dataclass

BASE_FEE_EUR = 90
RATE_PER_KG = {"ltl": 0.32, "ftl": 0.11, "container": 0.07}
RATE_PER_M3 = 9
BODY_MULTIPLIER = {"tent": 1, "reef": 1.28, "adr": 1.4, "oversize": 1.55}


@dataclass(frozen=True)
class QuoteRange:
    min_eur: int
    max_eur: int


def calc_range(weight: float, volume: float, ship_type: str, body: str) -> QuoteRange:
    weight = max(weight, 0)
    volume = max(volume, 0)
    rate = RATE_PER_KG.get(ship_type, RATE_PER_KG["ltl"])
    body_multiplier = BODY_MULTIPLIER.get(body, 1)
    raw = (BASE_FEE_EUR + weight * rate + volume * RATE_PER_M3) * body_multiplier
    min_eur = max(int(round((raw * 0.85) / 10) * 10), 60)
    max_eur = max(int(round((raw * 1.25) / 10) * 10), 90)
    return QuoteRange(min_eur=min_eur, max_eur=max_eur)
