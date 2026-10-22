import os
import pickle
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CO₂ emissions prediction", page_icon="🚗", layout="wide")

HERE = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load():
    with open(os.path.join(HERE, "co2_model.pkl"), "rb") as f:
        return pickle.load(f)

@st.cache_data
def load_options():
    df = pd.read_csv(os.path.join(HERE, "CO2_Emissions_Canada.csv"))
    def steps(col):
        lo, hi = df[col].min(), df[col].max()
        return [round(x * 0.5, 1) for x in range(int(lo // 0.5), int(hi // 0.5) + 2)]
    return {
        "engine": sorted(df["Engine Size(L)"].unique().tolist()),
        "cyl": sorted(int(c) for c in df["Cylinders"].unique()),
        "city": steps("Fuel Consumption City (L/100 km)"),
        "hwy": steps("Fuel Consumption Hwy (L/100 km)"),
    }

bundle = load()
model, features = bundle["model"], bundle["features"]
opts = load_options()
enc = model.named_steps["prep"].named_transformers_["cat"].named_steps["oh"]
cats = dict(zip(["Make", "Vehicle Class", "Transmission", "Fuel Type"], enc.categories_))
FUEL = {"X": "Regular gasoline", "Z": "Premium gasoline", "D": "Diesel",
        "E": "Ethanol (E85)", "N": "Natural gas"}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif:wght@600;700&family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"], .stApp {font-family: Inter, system-ui, sans-serif;}
.stApp {
  background: radial-gradient(ellipse at 15% 0%, #15233f 0%, transparent 45%),
              radial-gradient(ellipse at 100% 0%, #2a1219 0%, transparent 40%), #070b14;
  color: #e8ecf4;
}
header[data-testid="stHeader"], footer, #MainMenu {display:none !important;}
.block-container {max-width: 1100px; padding-top: 5.5rem; padding-bottom: 4rem;}
.badge {position: fixed; top: 18px; left: 22px; z-index: 99; display:flex; align-items:center; gap:10px;
  background:#0d1424cc; border:1px solid #1a2233; border-radius:12px; padding:10px 16px;}
.badge .dot {width:9px; height:9px; border-radius:50%; background:#20c997; box-shadow:0 0 8px #20c997;}
.badge b {display:block; font-size:.95rem; color:#e8ecf4;} .badge small {color:#8a93a6; font-size:.78rem;}
.title {font-family:'Noto Serif', Georgia, serif; font-size:clamp(2rem,5vw,3.4rem); text-align:center; margin:0; font-weight:700;
  background:linear-gradient(90deg,#ffdfe3 0%,#ffdfe3 40%,#ff7a85 75%,#ff8f8f 100%);
  -webkit-background-clip:text !important; background-clip:text !important; color:transparent !important; -webkit-text-fill-color:transparent;}
.sub {text-align:center; color:#8a93a6; margin:14px 0 0; font-size:1.05rem;}
.rule {width:360px; max-width:70%; height:1px; margin:28px auto 36px; background:linear-gradient(90deg,transparent,#ff5a67,transparent);}
div[data-testid="stVerticalBlockBorderWrapper"] {background:#0b111d; border:1px solid #1a2233 !important; border-radius:14px; padding:6px 4px; min-height:190px;}
.card-title {font-weight:600; font-size:1.05rem; margin:0 0 4px; color:#e8ecf4;}
.card-help {color:#8a93a6; font-size:.88rem; line-height:1.5; margin:0; min-height:4.6em;}
div[data-baseweb="select"] > div {background:#f1f3f7 !important; border-radius:10px !important; border:0 !important; min-height:46px;}
div[data-baseweb="select"] * {color:#0b0b0b !important;}
div[data-baseweb="select"] input::placeholder {color:#8a93a6 !important; opacity:1;}
.note {color:#5d667a; font-size:.92rem; margin:18px 0 0;}
div[data-testid="stElementContainer"]:has(> div.stButton), div.stElementContainer:has(> div.stButton) {display:flex; justify-content:center; width:100% !important;}
div.stButton {text-align:center; margin-top:18px;}
div.stButton > button {margin:0 auto; display:block;}
div.stButton > button {width:300px; max-width:100%; margin:0 auto; padding:.9rem 1.8rem; border:0; border-radius:14px; color:#fff; font-weight:600; font-size:1.05rem;
  background:linear-gradient(90deg,#ff4f5e,#ff7a59); box-shadow:0 0 34px #ff4f5e66;}
div.stButton > button:hover {filter:brightness(1.08); color:#fff; border:0;}
.res {margin:30px auto 0; max-width:520px; text-align:center; background:#0b111d; border:1px solid #ff5a6766;
  border-radius:16px; padding:24px; box-shadow:0 0 30px #ff4f5e22;}
.res small {color:#8a93a6;} .res .v {font-family:'Noto Serif', Georgia, serif; font-size:3rem; margin:6px 0; color:#ffb3ba;}
.bar {height:8px; border-radius:6px; background:#1a2233; margin:14px 0; overflow:hidden;}
.bar i {display:block; height:100%; background:linear-gradient(90deg,#20c997,#ffd166,#ff4f5e);}
.err {text-align:center; color:#ff8f8f; margin-top:20px;}
</style>
<div class="badge"><span class="dot"></span><div><b>Abdul Manan</b><small>FA24-BSE-001</small></div></div>
<h1 class="title">CO₂ emissions prediction</h1>
<p class="sub">Pick a value in each box, then press Predict.</p>
<div class="rule"></div>
""", unsafe_allow_html=True)

def card(col, title, key, options, help_text, fmt=None):
    with col:
        with st.container(border=True):
            st.markdown(f'<p class="card-title">{title}</p>', unsafe_allow_html=True)
            val = st.selectbox(title, options, index=None, placeholder="Click to choose",
                               key=key, label_visibility="collapsed", format_func=fmt or str)
            st.markdown(f'<p class="card-help">{help_text}</p>', unsafe_allow_html=True)
    return val

r1 = st.columns(4)
make = card(r1[0], "Make", "make", list(cats["Make"]), "Vehicle manufacturer")
vclass = card(r1[1], "Vehicle class", "vc", list(cats["Vehicle Class"]), "Body style and size of the vehicle")
trans = card(r1[2], "Transmission", "tr", list(cats["Transmission"]), "A automatic, M manual, AS auto-shift; number = gears")
fuel = card(r1[3], "Fuel type", "ft", list(cats["Fuel Type"]), "X regular, Z premium, D diesel, E ethanol, N natural gas",
            fmt=lambda k: f"{k} – {FUEL.get(k, k)}")
st.write("")
r2 = st.columns(4)
engine = card(r2[0], "Engine size", "en", opts["engine"], "Engine displacement in litres")
cyl = card(r2[1], "Cylinders", "cy", opts["cyl"], "Number of engine cylinders")
city = card(r2[2], "City consumption", "ci", opts["city"], "Fuel use in the city (L/100 km)")
hwy = card(r2[3], "Highway consumption", "hw", opts["hwy"], "Fuel use on the highway (L/100 km)")

st.markdown('<p class="note">Any combination can be chosen. Combined consumption is calculated as 55% city + 45% highway.</p>',
            unsafe_allow_html=True)

if st.button("Predict"):
    vals = [make, vclass, trans, fuel, engine, cyl, city, hwy]
    if any(v is None for v in vals):
        st.markdown('<p class="err">Please choose a value in every box.</p>', unsafe_allow_html=True)
    else:
        comb = round(0.55 * city + 0.45 * hwy, 1)
        row = pd.DataFrame([{
            "Make": make, "Vehicle Class": vclass, "Transmission": trans, "Fuel Type": fuel,
            "Engine Size(L)": engine, "Cylinders": cyl,
            "Fuel Consumption City (L/100 km)": city,
            "Fuel Consumption Hwy (L/100 km)": hwy,
            "Fuel Consumption Comb (L/100 km)": comb}])[features]
        pred = float(model.predict(row)[0])
        st.markdown(f"""<div class="res"><small>Predicted CO₂ emissions ({bundle['name']})</small>
        <div class="v">{pred:.0f} g/km</div>
        <div class="bar"><i style="width:{min(pred / 522 * 100, 100):.0f}%"></i></div>
        <small>Typical range in the data: 96 – 522 g/km</small></div>""", unsafe_allow_html=True)
