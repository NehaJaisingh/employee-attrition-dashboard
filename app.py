import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Workforce Intelligence Platform",
    page_icon="📈",
    layout="wide"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>

/* Main App */
.stApp {
    background: linear-gradient(to bottom right, #0f172a, #111827);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Remove Streamlit menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Hero Title */
.hero-title {
    font-size: 52px;
    font-weight: 800;
    color: white;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Glass Cards */
.glass-card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 20px;
}

/* Metrics */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px;
}

/* Buttons */
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.8rem;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
}

/* Inputs */
.stNumberInput input,
.stTextInput input,
textarea,
select {
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
    background-color: #1e293b !important;
    color: white !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 15px;
    color: white;
}

.stTabs [aria-selected="true"] {
    background: #2563eb !important;
}

/* Section Headings */
.section-title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 15px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

/* Footer */
.footer {
    color: #64748b;
    text-align: center;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
data = pd.read_csv("hr_attrition_dataset.csv")

data["AttritionReason"] = data["AttritionReason"].fillna("No Attrition")

if "EmployeeID" in data.columns:
    data = data.drop("EmployeeID", axis=1)

# ================= PREDICTION FUNCTION =================
def predict_employee(row):

    score = 0
    reasons = []

    if row["MonthlyIncome"] < 3000:
        score += 2
        reasons.append("Compensation Risk")

    if row["WorkLifeBalance"] <= 2:
        score += 2
        reasons.append("Poor Work-Life Balance")

    if row["OverTime"] == "Yes":
        score += 2
        reasons.append("Excessive Overtime")

    if row["StressLevel"] >= 7:
        score += 2
        reasons.append("High Stress Levels")

    if row["JobSatisfaction"] <= 2:
        score += 2
        reasons.append("Low Job Satisfaction")

    if score >= 6:
        return "High Risk", "3 Months", reasons

    elif score >= 3:
        return "Moderate Risk", "6 Months", reasons

    else:
        return "Low Risk", "-", reasons

# ================= HERO SECTION =================
st.markdown("""
<div class="hero-title">
Workforce Intelligence Platform
</div>

<div class="hero-subtitle">
Enterprise-grade employee attrition analytics dashboard designed for HR strategy and workforce retention insights.
</div>
""", unsafe_allow_html=True)

# ================= TABS =================
tab1, tab2, tab3 = st.tabs([
    "📊 Executive Dashboard",
    "🧠 Attrition Prediction",
    "📁 Workforce Database"
])

# ================= DASHBOARD TAB =================
with tab1:

    results = []

    for _, row in data.iterrows():
        risk, _, _ = predict_employee(row)
        results.append(risk)

    data["Risk Level"] = results

    high = len(data[data["Risk Level"] == "High Risk"])
    moderate = len(data[data["Risk Level"] == "Moderate Risk"])
    low = len(data[data["Risk Level"] == "Low Risk"])

    st.markdown(
        '<div class="section-title">Key Workforce Metrics</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3 = st.columns(3)

    m1.metric("🔴 High Risk Employees", high)
    m2.metric("🟡 Moderate Risk Employees", moderate)
    m3.metric("🟢 Low Risk Employees", low)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    # BAR CHART
    with c1:

        st.markdown(
            '<div class="glass-card">',
            unsafe_allow_html=True
        )

        st.markdown("### Workforce Risk Distribution")

        fig1, ax1 = plt.subplots(figsize=(5,4))

        ax1.bar(
            ["High", "Moderate", "Low"],
            [high, moderate, low]
        )

        ax1.set_facecolor("#0f172a")

        st.pyplot(fig1)

        st.markdown("</div>", unsafe_allow_html=True)

    # PIE CHART
    with c2:

        st.markdown(
            '<div class="glass-card">',
            unsafe_allow_html=True
        )

        st.markdown("### Employee Segmentation")

        fig2, ax2 = plt.subplots(figsize=(5,4))

        ax2.pie(
            [high, moderate, low],
            labels=["High", "Moderate", "Low"],
            autopct='%1.1f%%'
        )

        st.pyplot(fig2)

        st.markdown("</div>", unsafe_allow_html=True)

# ================= PREDICTION TAB =================
with tab2:

    st.markdown(
        '<div class="section-title">Employee Risk Assessment</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:

        salary = st.number_input(
            "Monthly Income",
            value=3000
        )

        worklife = st.slider(
            "Work-Life Balance",
            1,
            4
        )

        overtime = st.selectbox(
            "OverTime Status",
            ["Yes", "No"]
        )

    with right:

        stress = st.slider(
            "Stress Level",
            1,
            10
        )

        satisfaction = st.slider(
            "Job Satisfaction",
            1,
            4
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Generate Prediction"):

        row = {
            "MonthlyIncome": salary,
            "WorkLifeBalance": worklife,
            "OverTime": overtime,
            "StressLevel": stress,
            "JobSatisfaction": satisfaction
        }

        risk, time, reasons = predict_employee(row)

        st.markdown(
            '<div class="glass-card">',
            unsafe_allow_html=True
        )

        st.markdown("## Prediction Outcome")

        if risk == "High Risk":

            st.error(
                f"🔴 High Attrition Risk • Estimated Timeline: {time}"
            )

        elif risk == "Moderate Risk":

            st.warning(
                f"🟡 Moderate Attrition Risk • Estimated Timeline: {time}"
            )

        else:

            st.success(
                "🟢 Low Attrition Risk"
            )

        if reasons:

            st.markdown("### Key Risk Factors")

            for reason in reasons:
                st.write(f"• {reason}")

        st.markdown("</div>", unsafe_allow_html=True)

# ================= DATABASE TAB =================
with tab3:

    st.markdown(
        '<div class="section-title">Employee Workforce Database</div>',
        unsafe_allow_html=True
    )

    search = st.text_input(
        "Search Employee Records"
    )

    if search:

        filtered = data[
            data.apply(
                lambda row:
                row.astype(str).str.contains(search).any(),
                axis=1
            )
        ]

        st.dataframe(
            filtered,
            use_container_width=True
        )

    else:

        st.dataframe(
            data,
            use_container_width=True
        )

# ================= FOOTER =================
st.markdown("""
<div class="footer">
Developed by Neha • Workforce Intelligence & Attrition Analytics Platform
</div>
""", unsafe_allow_html=True)