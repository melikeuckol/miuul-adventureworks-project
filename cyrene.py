import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# 1. PAGE CONFIG
# =========================================================
st.set_page_config(page_title="Cyrene Elite Engine", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #1F1326; color: #FDFEFE; }
[data-testid="stSidebar"] { background-color: #2D1B36; border-right: 1px solid #E84E89; }
h1, h2, h3 { color: #E84E89 !important; }
div[data-testid="stMetricValue"] { color: #FDFEFE !important; }
div[data-testid="metric-container"] {
    background-color: rgba(232, 78, 137, 0.1);
    border: 1px solid #E84E89;
    padding: 15px;
    border-radius: 10px;
}
.login-box {
    background-color:#2D1B36;
    padding:40px;
    border-radius:15px;
    border:1px solid #E84E89;
    max-width: 400px;
    margin: 5rem auto;
}
/* Logout butonu stili */
div.stButton > button:first-child {
    background-color: #E84E89;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: bold;
    transition: all 0.3s ease;
}
div.stButton > button:first-child:hover {
    background-color: #B04173;
    color: white;
    border: 1px solid #FF8C42;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. SIMPLE ANALYST LOGIN
# =========================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("## 🔐 Analyst Access Portal")
    username = st.text_input("Analyst ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "analyst" and password == "cyrene123":
            st.session_state.authenticated = True
            st.success("Access Granted")
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.authenticated:
    login()
    st.stop()

# =========================================================
# 3. LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    df_ai = pd.read_csv('b2c_ai_final_results.csv', sep=';', decimal=',')
    df_cluster = pd.read_csv('b2c_kabile_analizi_final_v3.csv', sep=';')
    full_df = df_ai.merge(df_cluster, on='Customer_Key', how='left')

    # ---- Kabile isimlerini İngilizceleştir (ESNEK YÖNTEM) ----
    # Önce orijinal isimleri temizleyip küçük harfe çeviriyoruz
    temp_tribe = full_df['Kabile_Ismi'].str.strip().str.lower()

    # Mapping sözlüğü (anahtarlar küçük harf ve temizlenmiş olmalı)
    tribe_mapping_clean = {
        "saf performansçılar": "Pure Riders",
        "donanımcılar": "Gear Lovers",
        "kombinciler (maceracı)": "Mix Riders",
        "stil ikonları": "Style Focus",
        "stil i̇konları": "Style Focus" 
    }

    # Eşlemeyi uygula, eşleşmeyenler için orijinal değeri koru
    full_df['Kabile_Ismi'] = temp_tribe.map(tribe_mapping_clean).fillna(full_df['Kabile_Ismi'])
    # -----------------------------------------------------------

    avg_monetary = full_df['Monetary'].mean()
    avg_prob = full_df['Value_Probability'].mean()

    def create_segment(row):
        if row['Monetary'] > avg_monetary and row['Value_Probability'] > avg_prob:
            return "⭐ Star"
        elif row['Monetary'] > avg_monetary and row['Value_Probability'] <= avg_prob:
            return "💰 High Value"
        elif row['Monetary'] <= avg_monetary and row['Value_Probability'] > avg_prob:
            return "🎯 Potential"
        else:
            return "⚠ Low"

    full_df['Segment_Custom'] = full_df.apply(create_segment, axis=1)
    return full_df

df = load_data()

# =========================================================
# 4. HEADER WITH LOGO + TEAM
# =========================================================
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.image("logo (1).png", width=120)

with col_title:
    st.markdown("""
    <h1>CYRENE ELITE ENGINE</h1>
    <p style='font-size:18px; color:#E84E89; margin-bottom:0;'>
    Real-Time VIP Expansion Command Center
    </p>
    <p style='font-size:14px; color:#B04173;'>
    Developed by Cyrene Data Collective
    </p>
    """, unsafe_allow_html=True)

st.write("---")

# =========================================================
# 5. SIDEBAR (Filters + Logout)
# =========================================================
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>CONTROL HUB</h2>", unsafe_allow_html=True)
    st.write("---")

    threshold = st.slider("VIP Probability Threshold", 0.0, 1.0, 0.30)

    kabile_list = ["All"] + list(df['Kabile_Ismi'].dropna().unique())
    secilen_kabile = st.selectbox("Select a Tribe:", kabile_list)

    st.write("---")
    # Logout butonu - stil CSS ile verildi
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# =========================================================
# 6. FILTER PIPELINES
# =========================================================
if secilen_kabile == "All":
    tribe_df = df.copy()
else:
    tribe_df = df[df['Kabile_Ismi'] == secilen_kabile]

activation_df = tribe_df[tribe_df['Value_Probability'] >= threshold]

# =========================================================
# 7. TOP METRICS
# =========================================================
m1, m2, m3 = st.columns(3)
m1.metric("Activated Customers", len(activation_df))
m2.metric("Activated Revenue ($)", f"{activation_df['Monetary'].sum():,.0f}")
m3.metric("Avg Activated Probability", f"{activation_df['Value_Probability'].mean():.2f}" if len(activation_df) > 0 else "0")

st.write("---")

# =========================================================
# 8. TABS
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Strategic Map", "🛡️ Tribe Intelligence", "🚀 VIP Expansion Simulator", "📊 Distribution Analysis"])

# Renk paleti (marka renkleriyle uyumlu)
color_map = {
    "⭐ Star": "#FFD700",        # Altın sarısı
    "💰 High Value": "#E84E89",  # Pembe
    "🎯 Potential": "#FF8C42",    # Turuncu
    "⚠ Low": "#B04173"            # Mor
}

# TAB 1 - Strategic Map
with tab1:
    st.subheader("Activation Quadrant")
    if len(activation_df) == 0:
        st.warning("No customers meet the selected threshold.")
    else:
        fig = px.scatter(
            activation_df,
            x="Monetary",
            y="Value_Probability",
            color="Segment_Custom",
            color_discrete_map=color_map,
            hover_data=['Customer_Key', 'Kabile_Ismi'],
            template="plotly_dark"
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#FDFEFE"
        )
        st.plotly_chart(fig, use_container_width=True)

# TAB 2 - Tribe Intelligence (with segment distribution)
with tab2:
    st.subheader("Structural Tribe Profile")
    if not tribe_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tribe Customers", f"{len(tribe_df):,}")
        col2.metric("Avg Monetary ($)", f"{tribe_df['Monetary'].mean():,.0f}")
        col3.metric("Avg Probability", f"{tribe_df['Value_Probability'].mean():.2f}")
        high_ratio = (tribe_df['Value_Probability'] >= 0.6).mean() * 100
        col4.metric("High Prob. Ratio (%)", f"{high_ratio:.1f}%")

        st.markdown("#### Segment Distribution in Selected Tribe")
        segment_counts = tribe_df['Segment_Custom'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        fig2 = px.pie(
            segment_counts,
            values='Count',
            names='Segment',
            color='Segment',
            color_discrete_map=color_map,
            template="plotly_dark"
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#FDFEFE",
            showlegend=True
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Ek olarak, seçilen kabilenin probability dağılımı
        st.markdown("#### Probability Distribution in Tribe")
        fig3 = px.histogram(
            tribe_df,
            x="Value_Probability",
            nbins=30,
            color_discrete_sequence=["#E84E89"],
            template="plotly_dark"
        )
        fig3.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#FDFEFE",
            xaxis_title="Value Probability",
            yaxis_title="Count"
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("No data available for the selected tribe.")

# TAB 3 - VIP Expansion Simulator
with tab3:
    st.subheader("Conversion Scenario")
    potential_df = activation_df[activation_df['Segment_Custom'] == "🎯 Potential"]
    conversion_rate = st.slider("Conversion Rate (%)", 1, 50, 15)
    projected_new_vips = int(len(potential_df) * conversion_rate / 100)
    st.metric("Projected New VIPs", projected_new_vips)

    # Gelişmiş simülasyon: Tüm segmentler için dönüşüm
    st.markdown("#### Segment-based Conversion Simulation")
    seg_conv = {}
    for seg in color_map.keys():
        seg_df = activation_df[activation_df['Segment_Custom'] == seg]
        default_rate = 10 if seg == "🎯 Potential" else 5
        rate = st.slider(f"{seg} Conversion Rate (%)", 0, 100, default_rate, key=seg)
        seg_conv[seg] = int(len(seg_df) * rate / 100)
    total_projected = sum(seg_conv.values())
    st.metric("Total Projected VIPs from All Segments", total_projected)

# TAB 4 - Distribution Analysis (yeni)
with tab4:
    st.subheader("Overall Value Probability Distribution")
    fig4 = px.histogram(
        tribe_df,
        x="Value_Probability",
        nbins=40,
        color_discrete_sequence=["#FF8C42"],
        template="plotly_dark",
        title="Probability Distribution (All Tribes)" if secilen_kabile=="All" else f"Probability Distribution - {secilen_kabile}"
    )
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#FDFEFE"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("#### Top 10 Customers by Probability")
    top10 = tribe_df.nlargest(10, 'Value_Probability')[['Customer_Key', 'Kabile_Ismi', 'Monetary', 'Value_Probability', 'Segment_Custom']]
    st.dataframe(top10.style.format({'Monetary': '${:,.0f}', 'Value_Probability': '{:.2f}'}), use_container_width=True)

# =========================================================
# LIVE ELITE COUNTER - Düzeltildi: Artık tüm "Star"ları sayıyor (tribe_df içinden)
# =========================================================
elite_count = len(tribe_df[tribe_df['Segment_Custom'] == "⭐ Star"])

st.markdown(f"""
<div style='text-align:center; font-size:26px; padding:20px;
background-color:rgba(255,140,66,0.1);
border-radius:15px;
border:1px solid #FF8C42;'>
🏆 Active Elite VIP Identified: <strong>{elite_count}</strong>
</div>
""", unsafe_allow_html=True)

st.write("---")
st.markdown("""
<div style='text-align:center; padding:15px; font-size:14px; color:#B04173;'>
Cyrene is not a dashboard.  
It is a strategic decision engine.
</div>
""", unsafe_allow_html=True)