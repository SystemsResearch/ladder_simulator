from dataclasses import dataclass

@dataclass(frozen=True)
class Outcome:
    code: str
    label: str
    home_points: int
    away_points: int
    home_win_delta: int
    away_win_delta: int
    home_pd_delta: int
    away_pd_delta: int

OUTCOMES = [
    Outcome("HW", "Home win", 4, 0, 1, 0, 1, -1),
    Outcome("HW_HB", "Home win + home try bonus", 5, 0, 1, 0, 1, -1),
    Outcome("HW_ALB", "Home win + away losing bonus", 4, 1, 1, 0, 1, -1),
    Outcome("HW_HB_ALB", "Home win + home try bonus + away losing bonus", 5, 1, 1, 0, 1, -1),
    Outcome("AW", "Away win", 0, 4, 0, 1, -1, 1),
    Outcome("AW_AB", "Away win + away try bonus", 0, 5, 0, 1, -1, 1),
    Outcome("AW_HLB", "Away win + home losing bonus", 1, 4, 0, 1, -1, 1),
    Outcome("AW_AB_HLB", "Away win + away try bonus + home losing bonus", 1, 5, 0, 1, -1, 1),
    Outcome("D", "Draw", 2, 2, 0, 0, 0, 0),
    Outcome("D_HB", "Draw + home try bonus", 3, 2, 0, 0, 0, 0),
    Outcome("D_AB", "Draw + away try bonus", 2, 3, 0, 0, 0, 0),
    Outcome("D_BOTHB", "Draw + both try bonuses", 3, 3, 0, 0, 0, 0),
]

OUTCOME_CODES = [o.code for o in OUTCOMES]
HOME_POINTS = [o.home_points for o in OUTCOMES]
AWAY_POINTS = [o.away_points for o in OUTCOMES]
OUTCOME_LABELS = {o.code: o.label for o in OUTCOMES}

HOME_WIN_DELTA = [o.home_win_delta for o in OUTCOMES]
AWAY_WIN_DELTA = [o.away_win_delta for o in OUTCOMES]
HOME_PD_DELTA = [o.home_pd_delta for o in OUTCOMES]
AWAY_PD_DELTA = [o.away_pd_delta for o in OUTCOMES]
