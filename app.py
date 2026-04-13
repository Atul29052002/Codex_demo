import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Narration Generator", page_icon="🧠", layout="wide")


def make_synthetic_data(months: int = 12, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=months, freq="M")
    base = np.linspace(95000, 130000, months)
    seasonality = 9000 * np.sin(np.linspace(0, 2 * np.pi, months))
    noise = rng.normal(0, 4000, months)
    revenue = np.maximum(base + seasonality + noise, 1000)
    target = np.linspace(100000, 125000, months)
    return pd.DataFrame({"Month": dates, "Revenue": revenue.round(0), "Target": target.round(0)})


def generate_narration(df: pd.DataFrame) -> str:
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    mom_pct = ((latest["Revenue"] - prev["Revenue"]) / prev["Revenue"]) * 100
    target_gap = latest["Revenue"] - latest["Target"]
    avg_revenue = df["Revenue"].mean()

    direction = "increased" if mom_pct >= 0 else "declined"
    target_status = "above" if target_gap >= 0 else "below"

    return (
        f"In {latest['Month'].strftime('%B %Y')}, revenue was ${latest['Revenue']:,.0f}, "
        f"which {direction} by {abs(mom_pct):.1f}% month-over-month. "
        f"Performance landed ${abs(target_gap):,.0f} {target_status} target. "
        f"Average monthly revenue across the period is ${avg_revenue:,.0f}. "
        f"Recommended action: prioritize channels driving the strongest recent growth "
        f"and review underperforming segments if target attainment remains inconsistent."
    )


st.title("🧠 Analytics Report Narration Generator")
st.caption("Simple Streamlit UI demo with synthetic KPI data and auto-written narration.")

left, right = st.columns([1, 2])

with left:
    st.subheader("Settings")
    months = st.slider("Number of months", min_value=6, max_value=36, value=12)
    seed = st.number_input("Random seed", min_value=1, max_value=1000, value=7)

    if st.button("Generate Report"):
        st.session_state["df"] = make_synthetic_data(months=months, seed=seed)

if "df" not in st.session_state:
    st.session_state["df"] = make_synthetic_data()

df = st.session_state["df"]

with right:
    st.subheader("Revenue vs Target")
    st.line_chart(df.set_index("Month")[["Revenue", "Target"]])

st.subheader("Data Preview")
st.dataframe(df, use_container_width=True)

st.subheader("Generated Narration")
st.success(generate_narration(df))
