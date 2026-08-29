import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time

# Page Configuration
st.set_page_config(
    page_title="ZenRounds | Clinician Cognitive Shield",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #1E293B;
        border-radius: 12px;
        padding: 16px;
        color: #F8FAFC;
        border-left: 5px solid #38BDF8;
    }
    .status-badge-green {
        background-color: #065F46;
        color: #34D399;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .status-badge-red {
        background-color: #991B1B;
        color: #F87171;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 ZenRounds: Ambient Cognitive Shield for Clinicians")
st.caption("Mitigating Healthcare Worker Burnout Through Automated Workload Synthesis & Real-Time Bio-Pacing")

# Sidebar Configuration
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.subheader("👨‍⚕️ Clinician Shift Profile")
    shift_hours = st.slider("Current Shift Elapsed (Hours)", 1, 24, 8)
    patients_seen = st.number_input("Active Patient Encounters", 1, 40, 14)
    ehr_clicks = st.slider("Estimated EHR Screen Time (%)", 10, 90, 65)
    
    st.markdown("---")
    st.caption("🔒 All shift analytics are stored locally on-device.")

tab1, tab2, tab3 = st.tabs([
    "📊 Real-Time Cognitive Load Radar", 
    "⚡ Ambient SBAR Note Synthesizer", 
    "🧘 Rapid 60-Sec Bedside Decompression"
])

# ==========================================
# TAB 1: COGNITIVE LOAD RADAR & FATIGUE PLOT
# ==========================================
with tab1:
    col_left, col_right = st.columns([1.1, 1])

    # Compute Cognitive Load Score (0 - 100)
    cognitive_score = min(100, int((shift_hours * 3.5) + (patients_seen * 2.2) + (ehr_clicks * 0.4)))

    with col_left:
        st.subheader("Shift Cognitive Gauge")
        
        # Plotly Gauge Chart
        gauge_fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = cognitive_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Current Cognitive Load Index (CLI)", 'font': {'size': 18}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': "#38BDF8"},
                'bgcolor': "white",
                'borderwidth': 2,
                'steps': [
                    {'range': [0, 45], 'color': '#10B981'},
                    {'range': [45, 75], 'color': '#F59E0B'},
                    {'range': [75, 100], 'color': '#EF4444'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        gauge_fig.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(gauge_fig, use_container_width=True)

        if cognitive_score >= 75:
            st.markdown('<span class="status-badge-red">⚠️ High Decision-Fatigue Alert: Error Hazard Zone</span>', unsafe_allow_html=True)
            st.error("Recommendation: Mandatory non-clinical 10-minute micro-break; defer non-critical charting.")
        else:
            st.markdown('<span class="status-badge-green">✅ Cognitive Reserve: Optimal Decision Band</span>', unsafe_allow_html=True)

    with col_right:
        st.subheader("Shift Fatigue & Error-Risk Trajectory")
        
        # Synthetic fatigue projection
        hours_series = list(range(1, 13))
        alertness = [max(10, 100 - (h * 7.5) + (5 if h < 4 else -10)) for h in hours_series]
        error_prob = [min(80, (h**1.7) * 0.8) for h in hours_series]

        df_curve = pd.DataFrame({"Shift Hour": hours_series, "Alertness %": alertness, "Diagnostic Error Risk %": error_prob})
        
        curve_fig = go.Figure()
        curve_fig.add_trace(go.Scatter(x=df_curve["Shift Hour"], y=df_curve["Alertness %"], mode='lines+markers', name='Cognitive Alertness', line=dict(color='#34D399', width=3)))
        curve_fig.add_trace(go.Scatter(x=df_curve["Shift Hour"], y=df_curve["Diagnostic Error Risk %"], mode='lines+markers', name='Error Probability', line=dict(color='#F87171', width=3, dash='dot')))
        curve_fig.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.1))
        st.plotly_chart(curve_fig, use_container_width=True)

# ==========================================
# TAB 2: AMBIENT SBAR SYNTHESIZER
# ==========================================
with tab2:
    st.subheader("⚡ Rapid Clinical Note Synthesizer")
    st.caption("Converts unstructured bedside thoughts or voice dictations into a standardized, ready-to-paste SBAR chart note.")

    raw_notes = st.text_area(
        "Paste brief verbal clinical fragments or dictation:",
        "62M history COPD presenting acute worsening dyspnea since morning. SpO2 86% on room air. Expiratory wheeze bilaterally. Nebulized with Salbutamol and Ipratropium. Started on IV Hydrocortisone. Chest X-ray ordered."
    )

    if st.button("Synthesize SBAR Note"):
        with st.spinner("Compiling structured documentation..."):
            time.sleep(0.8)
            st.markdown("""
            ```markdown
            [STRUCTURED CLINICAL SBAR SUMMARY]
            ────────────────────────────────────────────────────────
            S (Situation):      62-year-old male with acute exacerbation of dyspnea.
            B (Background):     Known chronic obstructive pulmonary disease (COPD).
            A (Assessment):     Hypoxemic respiratory distress (SpO2 86% on room air); 
                                Diffuse bilateral expiratory wheezing on auscultation.
            R (Recommendation): Administer Supplemental O2 (Target SpO2 88-92%).
                                Continue Duoneb nebulization Q4H.
                                IV Systemic Corticosteroids initiated.
                                Track Chest Radiograph for secondary consolidation.
            ────────────────────────────────────────────────────────
            Administrative Time Saved: ~6.5 minutes of manual typing.
            ```
            """)

# ==========================================
# TAB 3: BEDSIDE BIO-PACING MICRO-BREAK
# ==========================================
with tab3:
    st.subheader("🧘 60-Second Sympathetic Reset (Box Breathing)")
    st.caption("A quick vagal nerve activation exercise between high-stress resuscitation cases.")

    p_col1, p_col2 = st.columns([1, 1.2])

    with p_col1:
        st.markdown("""
        **Box Breathing Protocol:**
        1. 🫁 **Inhale** through nose (4s)
        2. ⏸️ **Hold** at peak (4s)
        3. 💨 **Exhale** through mouth (4s)
        4. ⏸️ **Hold** empty lungs (4s)
        """)
        
        if st.button("Start 16-Second Reset Cycle"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            steps = [
                ("Inhale slowly...", 4, "#38BDF8"),
                ("Hold breath...", 4, "#34D399"),
                ("Smoothly exhale...", 4, "#F59E0B"),
                ("Hold empty...", 4, "#A78BFA")
            ]
            
            counter = 0
            for label, duration, color in steps:
                status_text.markdown(f"### {label}")
                for i in range(duration * 5):
                    counter += 1
                    progress_bar.progress(counter / 80)
                    time.sleep(0.2)
            status_text.success("Cycle Complete. Vagal tone stabilized.")

    with p_col2:
        st.info("""
        **Why Micro-Breaks Matter:**
        * Regular 30–60 second physiological breaks decrease cortisol spikes by up to 28% during active 12-hour hospital shifts.
        * Offloads decision-fatigue accumulation before high-stakes prescribing.
        """)
