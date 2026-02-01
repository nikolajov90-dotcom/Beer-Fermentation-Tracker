import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

def srm_to_rgb(srm):
    r = max(0, min(255, int(255 * (0.975 ** srm))))
    g = max(0, min(255, int(245 * (0.88 ** srm))))
    b = max(0, min(255, int(220 * (0.7 ** srm))))
    return r, g, b

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

st.markdown("""
<style>

/* cela aplikacija */
.stApp {
    background: transparent;
}

/* glavni streamlit wrapper */
section[data-testid="stMain"] {
    background: transparent;
}


</style>
""", unsafe_allow_html=True)


tab_cfu, tab_color, tab_ref = st.tabs(
    ["Praćenje toka fermentacije (CFU)", "Izračunavanje obojenosti piva (EBC/SRM)", "Skala obojenosti"]
)


with tab_cfu:
    st.title("CFU metoda")
    st.markdown("***Osnovi biotehnologije 2025/26***")

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

with tab_color:

    st.header("Spektrofotometrijsko merenje obojenosti")

    od430 = st.number_input(
        "Vrednost absorbance na 430 nm (OD₄₃₀)",
        min_value=0.0,
        step=0.01
    )

    if od430 > 0:
        ebc = 25 * od430
        srm = ebc / 1.97

        rgb = srm_to_rgb(srm)
        hex_color = rgb_to_hex(rgb)

        st.metric("EBC", f"{ebc:.1f}")
        st.metric("SRM", f"{srm:.1f}")

        st.markdown(
            f"""
            <div style="
                width: 120px;
                height: 120px;
                background-color: {hex_color};
                border: 1px solid black;
            ">
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "Izračunata obojenost predstavlja približu vrednost u odnosu na referentne EBC/SRM standarde."
        )
with tab_ref:

    st.header("EBC / SRM referentne skale")

    ref = [
        ("Pale Lager", 2, 4),
        ("Pilsner", 3, 5),
        ("Wheat beer", 5, 9),
        ("Pale Ale", 8, 14),
        ("Amber Ale", 12, 22),
        ("Brown Ale", 20, 35),
        ("Porter", 30, 60),
        ("Stout", 40, 80),
    ]

    for name, ebc_min, ebc_max in ref:
        srm_mid = ((ebc_min + ebc_max) / 2) / 1.97
        color = rgb_to_hex(srm_to_rgb(srm_mid))

        st.markdown(
            f"""
            <div style="display:flex; align-items:center; margin-bottom:6px;">
                <div style="
                    width:40px; height:40px;
                    background:{color};
                    border:1px solid black;
                    margin-right:10px;
                "></div>
                <b>{name}</b> — {ebc_min}–{ebc_max} EBC
            </div>
            """,
            unsafe_allow_html=True
        )
