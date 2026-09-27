"""
AgriN — Regenerative Agricultural Intelligence Network
Streamlit version | Track 4, BRICS Cooperation | Team Sarcastic

Run locally:
    pip install -r requirements.txt
    streamlit run app.py

Deploy free on Streamlit Community Cloud:
    1. Push this folder to your GitHub repo
    2. Go to https://share.streamlit.io -> New app -> pick the repo -> main file: app.py
    3. Done — you get a public https://<name>.streamlit.app link

Optional: set an ANTHROPIC_API_KEY as a Streamlit secret to enable live AI
recommendations and vision-based disease diagnosis. Without it, the app
runs fully on the rule-based / heuristic fallback — nothing breaks.
"""

import os
import io
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from PIL import Image

# ---------------------------------------------------------------------------
# Optional AI layer (Claude). Degrades gracefully if no key is configured.
# ---------------------------------------------------------------------------
AI_ENABLED = False
try:
    import anthropic
    _api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not _api_key:
        try:
            _api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
        except Exception:
            _api_key = None
    if _api_key:
        client = anthropic.Anthropic(api_key=_api_key)
        AI_ENABLED = True
except Exception:
    AI_ENABLED = False

# ---------------------------------------------------------------------------
# Page config + theme (Navy + Sage, matching the AgriN brand)
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AgriN — Regenerative Agricultural Intelligence", page_icon="🌾", layout="wide")

NAVY, NAVY2, SAGE, SAGE_DK, BRONZE, PAPER = "#121B30", "#1C2A47", "#8FA98C", "#5F7A5C", "#C9A15A", "#F3F4EE"

st.markdown(f"""
<style>
.stApp {{ background-color: {PAPER}; }}
[data-testid="stHeader"] {{ background-color: {NAVY}; }}
h1, h2, h3 {{ color: {NAVY} !important; font-family: Georgia, serif; }}
.stTabs [data-baseweb="tab"] {{ font-weight:600; }}
.agrin-hero {{ background: linear-gradient(135deg, {NAVY}, {NAVY2}); color:white; padding:22px 26px;
  border-radius:12px; margin-bottom:18px; }}
.agrin-hero .tag {{ color:{SAGE}; font-size:.78rem; letter-spacing:.04em; }}
div[data-testid="stMetricValue"] {{ color:{NAVY}; }}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="agrin-hero">
  <div class="tag">TRACK 4 · AgriN & REGENERATIVE AGRICULTURAL INTELLIGENCE · BRICS COOPERATION</div>
  <h1 style="color:white; margin:6px 0 4px;">🌾 AgriN</h1>
  <div style="color:{SAGE};">A shared digital agriculture network delivering real-time, AI-guided regenerative farming advice across BRICS nations.</div>
</div>
""", unsafe_allow_html=True)

if not AI_ENABLED:
    st.info("Running in rule-based demo mode. Add an `ANTHROPIC_API_KEY` secret to enable live AI recommendations and vision diagnosis.", icon="ℹ️")

# ---------------------------------------------------------------------------
# Shared regional data
# ---------------------------------------------------------------------------
REGION_DATA = {
    "Malwa Plateau, India":       {"soil": 72, "ndvi": 68, "rain": "64mm, next 5 days", "crop": "Soybean / Chana rotation", "comp": [38, 34, 28]},
    "Cerrado, Brazil":            {"soil": 65, "ndvi": 74, "rain": "12mm, dry spell",     "crop": "Cover-crop maize",        "comp": [30, 44, 26]},
    "Free State, South Africa":   {"soil": 58, "ndvi": 55, "rain": "8mm, drought watch",  "crop": "Sorghum",                 "comp": [46, 26, 28]},
    "Volga Basin, Russia":        {"soil": 70, "ndvi": 61, "rain": "22mm, cool front",    "crop": "Winter wheat",            "comp": [40, 32, 28]},
    "Heilongjiang, China":        {"soil": 77, "ndvi": 80, "rain": "40mm, monsoon tail",  "crop": "Rice / soybean",          "comp": [34, 40, 26]},
}

tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🤖 Crop Advisor", "🔬 Disease Scanner", "🌐 BRICS Network"])

# ---------------------------------------------------------------------------
# Tab 1 — Dashboard
# ---------------------------------------------------------------------------
with tab1:
    region = st.selectbox("Region", list(REGION_DATA.keys()))
    r = REGION_DATA[region]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Soil health index", f"{r['soil']}/100")
    c2.metric("Satellite NDVI", f"{r['ndvi']}/100")
    c3.metric("Weather forecast", r["rain"])
    c4.metric("Focus crop", r["crop"])

    colA, colB = st.columns([1.3, 1])
    with colA:
        st.subheader("30-day NDVI trend")
        days = [f"D-{90-i*10}" for i in range(10)]
        trend = [round(r["ndvi"] * 0.75 + i * (r["ndvi"] * 0.025) + np.sin(i) * 2, 1) for i in range(10)]
        fig = go.Figure(go.Scatter(x=days, y=trend, mode="lines", fill="tozeroy",
                                    line=dict(color=BRONZE, width=3)))
        fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    with colB:
        st.subheader("Soil composition")
        fig2 = go.Figure(go.Pie(labels=["Organic matter", "Minerals", "Moisture"], values=r["comp"],
                                 marker=dict(colors=[SAGE, NAVY, BRONZE]), hole=0.5))
        fig2.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)

    st.caption("Figures shown are illustrative for the prototype demo. Production pulls Sentinel-2/MODIS NDVI, "
               "national soil-health datasets, and regional weather-model forecasts through the shared BRICS AgriN data layer.")

# ---------------------------------------------------------------------------
# Tab 2 — Crop Advisor
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Regenerative Crop Advisor")
    col1, col2 = st.columns(2)
    soil_type = col1.selectbox("Soil type", ["Black cotton (clay-heavy)", "Alluvial", "Red laterite", "Sandy loam"])
    season = col2.selectbox("Season", ["Kharif (monsoon)", "Rabi (winter)", "Zaid (summer)"])
    rainfall = col1.selectbox("Avg. rainfall", ["Low (<500mm)", "Moderate (500–1000mm)", "High (>1000mm)"])
    priority = col2.selectbox("Land health priority", ["Soil carbon rebuilding", "Water conservation", "Maximise yield"])

    def rule_based_recommendation(soil, season, rain, priority):
        if "Black cotton" in soil and "Kharif" in season:
            return "Cotton intercropped with pigeon pea", ["Deep taproot pigeon pea breaks compacted clay", "Adds nitrogen back for next cycle"]
        if "Low" in rain:
            return "Pearl millet (bajra) with mulch cover", ["Drought-tolerant, low water need", "Mulching cuts evaporation loss"]
        if "carbon" in priority:
            return "Multi-species cover crop (legume + cereal mix)", ["Builds soil organic carbon fastest", "Rotate with cash crop next season"]
        if "Rabi" in season:
            return "Wheat–mustard intercrop", ["Mustard breaks pest cycles for wheat", "Efficient winter water use"]
        return "Sorghum with green manure rotation", ["Resilient across most soil types", "Green manure restores soil structure"]

    if st.button("Get recommendation", type="primary"):
        with st.spinner("Generating a regenerative recommendation..."):
            crop, tips, reasoning = None, [], ""
            if AI_ENABLED:
                try:
                    prompt = (f'You are an agronomist for a regenerative-agriculture advisory tool. Farmer\'s field: '
                              f'soil type "{soil_type}", season "{season}", rainfall "{rainfall}", stated land-health '
                              f'priority "{priority}". Respond ONLY with JSON: {{"crop":"short recommendation (max 8 words)",'
                              f'"reasoning":"1-2 sentence explanation","tips":["tip1","tip2","tip3"]}}')
                    msg = client.messages.create(model="claude-sonnet-4-6", max_tokens=300,
                                                  messages=[{"role": "user", "content": prompt}])
                    import json
                    out = json.loads(msg.content[0].text)
                    crop, tips, reasoning = out["crop"], out.get("tips", []), out.get("reasoning", "")
                except Exception:
                    crop = None
            if not crop:
                crop, tips = rule_based_recommendation(soil_type, season, rainfall, priority)

            st.success(f"**{crop}**")
            if reasoning:
                st.write(reasoning)
            for t in tips:
                st.markdown(f"- {t}")
            st.caption("AI-generated recommendation." if AI_ENABLED and reasoning else
                       "Matched against soil type, season, rainfall band and stated land-health priority (rule-based demo mode).")

# ---------------------------------------------------------------------------
# Tab 3 — Disease Scanner
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Crop Disease Diagnostic")
    st.caption("Upload a leaf photo. Demo mode runs an on-device colour/texture heuristic — the production build "
               "swaps in a trained CV model (YOLOv8/EfficientNet) served from the AgriN backend.")
    uploaded = st.file_uploader("Leaf image", type=["jpg", "jpeg", "png"])

    if uploaded:
        img = Image.open(uploaded).convert("RGB")
        st.image(img, width=220)
        with st.spinner("Analysing leaf image..."):
            small = np.array(img.resize((60, 60)))
            r_ch, g_ch, b_ch = small[:, :, 0].astype(int), small[:, :, 1].astype(int), small[:, :, 2].astype(int)
            green_mask = (g_ch > r_ch) & (g_ch > b_ch)
            brown_mask = (r_ch > 90) & (r_ch < 180) & (g_ch < r_ch * 0.8) & (b_ch < r_ch * 0.6)
            green_pct = round(100 * green_mask.mean())
            brown_pct = round(100 * brown_mask.mean())

            diagnosis, confidence, advice = None, None, []
            if AI_ENABLED:
                try:
                    import base64, json
                    buf = io.BytesIO(); img.save(buf, format="JPEG")
                    b64 = base64.b64encode(buf.getvalue()).decode()
                    msg = client.messages.create(model="claude-sonnet-4-6", max_tokens=300, messages=[{
                        "role": "user", "content": [
                            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}},
                            {"type": "text", "text": 'You are a plant-pathology assistant. Respond ONLY with JSON: '
                                                      '{"diagnosis":"short name or Healthy","confidence":0-100,"advice":["step1","step2","step3"]}'}
                        ]}])
                    out = json.loads(msg.content[0].text)
                    diagnosis, confidence, advice = out["diagnosis"], out["confidence"], out.get("advice", [])
                except Exception:
                    diagnosis = None

            if not diagnosis:
                if brown_pct > 18:
                    diagnosis, confidence = "Possible early blight / leaf spot", min(60 + brown_pct, 92)
                    advice = ["Isolate affected plants", "Apply copper-based fungicide within 48h", "Reduce overhead irrigation"]
                elif green_pct < 40:
                    diagnosis, confidence = "Possible nutrient stress (chlorosis)", 55
                    advice = ["Check nitrogen and magnesium levels", "Soil test recommended"]
                else:
                    diagnosis, confidence = "Leaf appears healthy", 88
                    advice = ["No action needed", "Recheck in 7 days"]

            st.success(f"**{diagnosis}**  ·  confidence {confidence}%")
            for a in advice:
                st.markdown(f"- {a}")
            st.caption(f"Heuristic signal: brown {brown_pct}% / green {green_pct}%. Not a clinical diagnosis." if not AI_ENABLED
                       else "AI vision analysis of the uploaded photo.")

# ---------------------------------------------------------------------------
# Tab 4 — BRICS Network
# ---------------------------------------------------------------------------
with tab4:
    st.subheader("BRICS Shared Intelligence Layer")
    st.caption("A common protocol for member nations to publish and subscribe to regenerative-agriculture models — "
               "soil taxonomies, pest-outbreak signals, and climate-resilient seed data — without centralising raw farm data.")

    nodes = {"India": (3, 2), "Brazil": (0.5, 0.5), "South Africa": (2, -0.5), "Russia": (4.2, 3), "China": (5.5, 1.5)}
    edge_x, edge_y = [], []
    names = list(nodes.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            x0, y0 = nodes[names[i]]; x1, y1 = nodes[names[j]]
            edge_x += [x0, x1, None]; edge_y += [y0, y1, None]

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(color=SAGE, width=1, dash="dot"), hoverinfo="none"))
    fig3.add_trace(go.Scatter(x=[v[0] for v in nodes.values()], y=[v[1] for v in nodes.values()],
                               mode="markers+text", text=names, textposition="bottom center",
                               marker=dict(size=18, color=BRONZE, line=dict(width=2, color="white"))))
    fig3.update_layout(height=340, showlegend=False, xaxis=dict(visible=False), yaxis=dict(visible=False),
                        margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Shared this quarter", "1,240", "soil-health model updates")
    c2.metric("Cross-border advisories", "86", "pest/disease alerts propagated")
    c3.metric("Member farms connected", "4.2K", "across 5 nations (demo figures)")

st.markdown("---")
st.caption("AgriN prototype · Track 4, BRICS Cooperation · Team Sarcastic · CodeForCommunities Hackathon 2026")
