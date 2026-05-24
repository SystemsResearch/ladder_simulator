# Super Rugby Pacific final standings simulator

Monte Carlo simulation using discrete ladder-point outcomes, and a simplified points differential as tie-breaker. Developed by Dimitri Perrin.

## Model

- Current competition points are taken from `data/standings.csv`.
- Remaining fixtures are taken from `data/fixtures.csv`.
- Each match is simulated using a 12-outcome ladder-point distribution:
  - home win with/without try bonus and losing bonus
  - away win with/without try bonus and losing bonus
  - draw with/without try bonuses
- Tie-breakers are applied after competition points in this order:
  1. total number of wins
  2. points differential (PD)
- PD is simplified: when a team wins, their PD increases by 1, and if they lose it decreases by 1.
- Rows are sorted by expected final finishing position.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deployed version

You can access the deployed version here: https://ladder-simulator.streamlit.app/
