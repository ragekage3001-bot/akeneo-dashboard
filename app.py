import streamlit as st
import pandas as pd
import random

st.set_page_config(layout="wide")

# -------------------------------
# SESSION STATE
# -------------------------------
# -------------------------------
# SESSION STATE
# -------------------------------
if "df" not in st.session_state:
    st.session_state.df = None

if "attrs" not in st.session_state:
    st.session_state.attrs = []

# -------------------------------
# MOCK DATA GENERATOR
# -------------------------------
def generate_mock_data(n=200):
    families = ["doors", "windows", "handles"]
    attributes = ["name", "description", "ean", "color", "material"]

    data = []

    for i in range(n):
        family = random.choice(families)

        if family == "doors":
            fill_rate = 0.4
        elif family == "windows":
            fill_rate = 0.7
        else:
            fill_rate = 0.9

        row = {
            "identifier": f"SKU_{i}",
            "family": family
        }

        for attr in attributes:
            if random.random() < fill_rate:
                row[attr] = f"{attr}_{i}"
            else:
                row[attr] = None

        data.append(row)

    return pd.DataFrame(data), attributes

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("Steuerung")

if st.sidebar.button("🧪 Daten laden"):
    df, attrs = generate_mock_data(300)
    st.session_state.df = df
    st.session_state.attrs = attrs

# -------------------------------
# MAIN
# -------------------------------
if st.session_state.df is not None:

    df = st.session_state.df
    attrs = st.session_state.attrs

    st.title("📊 Akeneo Data Quality Dashboard")

    # -------------------------------
    # SCORE
    # -------------------------------
    total = len(df)
    total_fields = total * len(attrs)

    filled = df[attrs].notna().sum().sum()
    completeness = (filled / total_fields) * 100

    score = round(completeness, 2)

    if score >= 80:
        status = "🟢 Gut"
    elif score >= 50:
        status = "🟡 Mittel"
    else:
        status = "🔴 Kritisch"

    st.metric("Datenqualität", f"{score}/100")
    st.write(status)

    # -------------------------------
    # CHART
    # -------------------------------
    st.subheader("Produkte pro Family")
    st.bar_chart(df["family"].value_counts())

    # -------------------------------
    # HEATMAP (STABIL + CLOUD SAFE)
    # -------------------------------
    st.subheader("🔥 Heatmap (Füllgrad in %)")

    grouped = df.groupby("family")
    result = []

    for family, group in grouped:
        row = {"family": family}

        for attr in attrs:
            pct = group[attr].notna().mean() * 100
            row[attr] = round(pct, 1)

        result.append(row)

    hm = pd.DataFrame(result).set_index("family")

    # 👉 WICHTIG: OHNE Styler → stabil in Streamlit Cloud
    st.dataframe(hm, use_container_width=True)

else:
    st.info("👉 Bitte links auf 'Daten laden' klicken")
streamlit
pandas
requests
matplotlib
