import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

st.title("Fermentation CFU Tracker")
st.markdown("""***Osnovi biotehnologije 2025/26***""")
def cfu_ml(colonies, dilution, plated_volume_ml):
    return colonies / (dilution * plated_volume_ml)
# Učitavanje pozadine
def set_bg(img_file):
    with open(img_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("background.jpg")

st.markdown("""
<style>

/* Pozadina aplikacije */
[data-testid="stAppViewContainer"] {
    background: transparent;
}

/* Glavni content panel */
[data-testid="stMainBlockContainer"] {
    background-color: rgba(255,255,255,0.85);
    padding: 2rem;
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stMainBlockContainer"] {
    background-color: rgba(255,255,255,0.85);
    box-shadow: 0px 0px 30px rgba(0,0,0,0.3);
}
[data-testid="stMainBlockContainer"] * {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Default: light panel */
[data-testid="stMainBlockContainer"] {
    background-color: rgba(255,255,255,0.85);
}
[data-testid="stMainBlockContainer"] * {
    color: black !important;
}

/* Dark mode adaptive */
@media (prefers-color-scheme: dark) {
  [data-testid="stMainBlockContainer"] {
    background-color: rgba(30,30,30,0.85);
  }
  [data-testid="stMainBlockContainer"] * {
    color: white !important;
  }
}

</style>
""", unsafe_allow_html=True)

# Session storage
if "data" not in st.session_state:
    st.session_state.data = []

st.header("Dodavanje merenja")

time_point = st.number_input("Vreme uzorkovanja (h)", min_value=0.0, step=1.0)
colonies = st.number_input("Broj kolonija", min_value=0, step=1)
dilution_exp = st.number_input("Eksponent razblaženja (za 10^-5 uneti 5)", min_value=1, step=1)
volume = st.number_input("Zasejani volumen (mL)", value=0.1)

if st.button("Dodaj merenje"):
    dilution = 10 ** (-dilution_exp)
    value = cfu_ml(colonies, dilution, volume)

    st.session_state.data.append({
        "Time (h)": time_point,
        "CFU/mL": value
    })

    st.success(f"Dodato: {value:.2e} CFU/mL")


st.header("Podaci")

if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)

    # proseci po vremenu
    df_avg = df.groupby("Time (h)").mean().reset_index()

    st.dataframe(df_avg)

    st.header("Kriva fermentacije")

    fig, ax = plt.subplots()
    ax.plot(df_avg["Time (h)"], df_avg["CFU/mL"], marker="o")
    ax.set_yscale("log")
    ax.set_xlabel("Vreme (h)")
    ax.set_ylabel("CFU/mL")
    ax.set_title("Rast kvasca tokom fermentacije")
    ax.grid(True)

    st.pyplot(fig)

    if st.button("Resetuj podatke"):
        st.session_state.data = []

