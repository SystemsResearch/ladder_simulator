# Super Rugby Pacific final standings simulator

A Streamlit app for simulating final Super Rugby Pacific ladder positions using Monte Carlo simulation.

## Model

- Current competition points are taken from `data/standings.csv`.
- Remaining fixtures are taken from `data/fixtures.csv`.
- Each match is simulated using a 12-outcome ladder-point distribution:
  - home win with/without try bonus and losing bonus
  - away win with/without try bonus and losing bonus
  - draw with/without try bonuses
- Tie-breaker: points differential (PD) is used after competition points. It is a largely frozen PD: when a team wins, their PD increases by 1, and if they lose it decreases by 1.
- Rows are sorted by expected final finishing position.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deployed version

You can access the deployed version here: https://ladder-simulator.streamlit.app/
