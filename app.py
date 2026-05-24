import pandas as pd
import plotly.express as px
import streamlit as st

from outcomes import OUTCOME_CODES, OUTCOME_LABELS
from simulation import default_fixture_distribution, simulate_final_standings

st.set_page_config(page_title="Super Rugby Pacific Simulator", layout="wide")

st.title("Super Rugby Pacific final standings simulator")
st.caption("Monte Carlo simulation using discrete ladder-point outcomes, frozen current points differential as tie-breaker.")

standings = pd.read_csv("data/standings.csv")
fixtures = pd.read_csv("data/fixtures.csv")

with st.sidebar:
    st.header("Simulation settings")
    n_sims = st.slider("Number of simulations", 1_000, 100_000, 10_000, step=1_000)
    seed = st.number_input("Random seed", min_value=0, value=42, step=1)
    advanced = st.toggle("Advanced probability mode", value=False)
    st.markdown("Rows are sorted by expected final ladder position.")

fixture_probs = {}

st.subheader("Remaining games")

for idx, row in fixtures.iterrows():
    with st.expander(f"{row['Home']} vs {row['Away']}", expanded=False):
        if not advanced:
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                home_win = st.slider("Home win probability", 0.0, 1.0, 0.50, 0.01, key=f"home_{idx}")
            with c2:
                draw = st.slider("Draw probability", 0.0, 0.20, 0.03, 0.01, key=f"draw_{idx}")
            with c3:
                try_bonus = st.slider("Try bonus tendency", 0.0, 1.0, 0.35, 0.01, key=f"tb_{idx}")
            with c4:
                losing_bonus = st.slider("Losing bonus tendency", 0.0, 1.0, 0.30, 0.01, key=f"lb_{idx}")

            fixture_probs[idx] = default_fixture_distribution(
                home_win_prob=home_win,
                draw_prob=draw,
                try_bonus_rate=try_bonus,
                losing_bonus_rate=losing_bonus,
            )
        else:
            st.write("Enter relative probabilities. They will be normalised automatically.")
            values = {}
            cols = st.columns(3)
            for i, code in enumerate(OUTCOME_CODES):
                with cols[i % 3]:
                    values[code] = st.number_input(
                        OUTCOME_LABELS[code],
                        min_value=0.0,
                        value=1.0,
                        step=0.1,
                        key=f"adv_{idx}_{code}",
                    )
            fixture_probs[idx] = values

prob_df, summary_df = simulate_final_standings(
    standings=standings,
    fixtures=fixtures,
    fixture_probs=fixture_probs,
    n_sims=n_sims,
    seed=int(seed),
)

st.subheader("Final position probability grid")

heatmap_data = prob_df * 100
fig = px.imshow(
    heatmap_data,
    labels=dict(x="Final position", y="Team", color="Probability (%)"),
    text_auto=".1f",
    aspect="auto",
)
fig.update_layout(height=620)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Summary")
summary_display = summary_df.copy()
summary_display["Expected finish"] = summary_display["Expected finish"].map(lambda x: f"{x:.2f}")
summary_display["Top 6 probability"] = summary_display["Top 6 probability"].map(lambda x: f"{100*x:.1f}%")
st.dataframe(summary_display, use_container_width=True, hide_index=True)

with st.expander("Current standings data"):
    st.dataframe(standings, use_container_width=True, hide_index=True)
