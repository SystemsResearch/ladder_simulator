# Super Rugby Pacific final standings simulator

A Streamlit app for simulating final Super Rugby Pacific ladder positions using Monte Carlo simulation.

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

## Deploy

Push this repository to GitHub, then deploy it through Streamlit Community Cloud.
