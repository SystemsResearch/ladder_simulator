from __future__ import annotations

import numpy as np
import pandas as pd

from outcomes import (
    OUTCOME_CODES,
    HOME_POINTS,
    AWAY_POINTS,
    HOME_WIN_DELTA,
    AWAY_WIN_DELTA,
    HOME_PD_DELTA,
    AWAY_PD_DELTA,
)


def normalise_probs(probs: np.ndarray) -> np.ndarray:
    probs = np.asarray(probs, dtype=float)
    total = probs.sum()
    if total <= 0:
        raise ValueError("Outcome probabilities must have positive total.")
    return probs / total


def default_fixture_distribution(
    home_win_prob: float = 0.50,
    draw_prob: float = 0.03,
    try_bonus_rate: float = 0.35,
    losing_bonus_rate: float = 0.30,
) -> dict[str, float]:
    """Create a 12-outcome distribution from simple controls.

    home_win_prob is conditional on the match not being drawn.
    try_bonus_rate and losing_bonus_rate apply to the winning side and losing side.
    In draws, each team independently receives a try bonus with try_bonus_rate.
    """
    draw_prob = float(np.clip(draw_prob, 0.0, 0.5))
    home_win_prob = float(np.clip(home_win_prob, 0.0, 1.0))
    try_bonus_rate = float(np.clip(try_bonus_rate, 0.0, 1.0))
    losing_bonus_rate = float(np.clip(losing_bonus_rate, 0.0, 1.0))

    non_draw = 1.0 - draw_prob
    hw = non_draw * home_win_prob
    aw = non_draw * (1.0 - home_win_prob)

    probs = {
        "HW": hw * (1 - try_bonus_rate) * (1 - losing_bonus_rate),
        "HW_HB": hw * try_bonus_rate * (1 - losing_bonus_rate),
        "HW_ALB": hw * (1 - try_bonus_rate) * losing_bonus_rate,
        "HW_HB_ALB": hw * try_bonus_rate * losing_bonus_rate,
        "AW": aw * (1 - try_bonus_rate) * (1 - losing_bonus_rate),
        "AW_AB": aw * try_bonus_rate * (1 - losing_bonus_rate),
        "AW_HLB": aw * (1 - try_bonus_rate) * losing_bonus_rate,
        "AW_AB_HLB": aw * try_bonus_rate * losing_bonus_rate,
        "D": draw_prob * (1 - try_bonus_rate) * (1 - try_bonus_rate),
        "D_HB": draw_prob * try_bonus_rate * (1 - try_bonus_rate),
        "D_AB": draw_prob * (1 - try_bonus_rate) * try_bonus_rate,
        "D_BOTHB": draw_prob * try_bonus_rate * try_bonus_rate,
    }
    return probs


def simulate_final_standings(
    standings: pd.DataFrame,
    fixtures: pd.DataFrame,
    fixture_probs: dict[int, dict[str, float]],
    n_sims: int = 10_000,
    seed: int | None = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return finishing-position probabilities and summary stats.

    Tie-breakers: competition points, then total wins, then simplified points differential.

    Wins start from the current ladder values. Each simulated win adds one win.
    Points differential starts from current PD, then receives a small result-based
    adjustment: +1 for a win, -1 for a loss, unchanged for a draw.
    """
    rng = np.random.default_rng(seed)

    teams = standings["Team"].tolist()
    team_to_idx = {team: i for i, team in enumerate(teams)}
    n_teams = len(teams)

    required_columns = {"Team", "Points", "Wins", "PD"}
    missing_columns = required_columns - set(standings.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"standings.csv is missing required column(s): {missing}")

    points = np.tile(standings["Points"].to_numpy(dtype=float), (n_sims, 1))
    wins = np.tile(standings["Wins"].to_numpy(dtype=float), (n_sims, 1))
    pdiff = np.tile(standings["PD"].to_numpy(dtype=float), (n_sims, 1))

    home_add = np.asarray(HOME_POINTS, dtype=float)
    away_add = np.asarray(AWAY_POINTS, dtype=float)
    home_win_add = np.asarray(HOME_WIN_DELTA, dtype=float)
    away_win_add = np.asarray(AWAY_WIN_DELTA, dtype=float)
    home_pd_add = np.asarray(HOME_PD_DELTA, dtype=float)
    away_pd_add = np.asarray(AWAY_PD_DELTA, dtype=float)

    for fixture_idx, row in fixtures.iterrows():
        home_idx = team_to_idx[row["Home"]]
        away_idx = team_to_idx[row["Away"]]

        prob_dict = fixture_probs[fixture_idx]
        probs = normalise_probs(np.array([prob_dict.get(code, 0.0) for code in OUTCOME_CODES]))
        sampled = rng.choice(len(OUTCOME_CODES), size=n_sims, p=probs)

        points[:, home_idx] += home_add[sampled]
        points[:, away_idx] += away_add[sampled]
        wins[:, home_idx] += home_win_add[sampled]
        wins[:, away_idx] += away_win_add[sampled]
        pdiff[:, home_idx] += home_pd_add[sampled]
        pdiff[:, away_idx] += away_pd_add[sampled]

    position_counts = np.zeros((n_teams, n_teams), dtype=int)

    # Sort by competition points, then total wins, then adjusted points differential.
    # np.lexsort uses the last key as primary; negative values give descending order.
    for s in range(n_sims):
        order = np.lexsort((-pdiff[s], -wins[s], -points[s]))
        for pos, team_idx in enumerate(order):
            position_counts[team_idx, pos] += 1

    probs = position_counts / n_sims
    prob_df = pd.DataFrame(
        probs,
        index=teams,
        columns=[f"{i + 1}" for i in range(n_teams)],
    )

    expected_finish = probs @ np.arange(1, n_teams + 1)
    finals_probability = probs[:, :6].sum(axis=1)

    summary_df = pd.DataFrame({
        "Team": teams,
        "Expected finish": expected_finish,
        "Top 6 probability": finals_probability,
    }).sort_values("Expected finish")

    prob_df = prob_df.loc[summary_df["Team"]]
    return prob_df, summary_df
