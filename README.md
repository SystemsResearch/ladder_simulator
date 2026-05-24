# Rugby - Final standings simulator

A Streamlit app for simulating final ladder positions using Monte Carlo simulation.

This is initially set up for Super Rugby Pacific (ladder, remaining games, bonus point and tie-breaker rules)

## Model

- Current competition points are taken from `data/standings.csv`.
- Remaining fixtures are taken from `data/fixtures.csv`.
- Each match is simulated using a 12-outcome ladder-point distribution:
  - home win with/without try bonus and losing bonus
  - away win with/without try bonus and losing bonus
  - draw with/without try bonuses
- Tie-breaker: current points differential is frozen and used after competition points.
- Rows are sorted by expected final finishing position.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
