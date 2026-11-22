

import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Credit Portfolio Intelligence",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. CUSTOM DASHBOARD DESIGN
# =====================================================


st.markdown("""
<style>

/* ==========================================
   1. MAIN DASHBOARD BACKGROUND
========================================== */

.stApp {
    background: #F1F5F9 !important;
    color: #172033 !important;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* ==========================================
   2. SIDEBAR DESIGN
========================================== */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #101D38 0%,
        #1E3A5F 100%
    ) !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] hr {
    border-color: #526783 !important;
}

/* ==========================================
   3. SIDEBAR CLUSTER DROPDOWN
   FIX: BLACK TEXT ALWAYS VISIBLE
========================================== */

/* Dropdown outer box */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}

/* Selected value: All Clusters, 0, 1, 2, 3 */
section[data-testid="stSidebar"] div[data-baseweb="select"] div,
section[data-testid="stSidebar"] div[data-baseweb="select"] span,
section[data-testid="stSidebar"] div[data-baseweb="select"] input {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

/* Dropdown arrow */
section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #000000 !important;
    color: #000000 !important;
}

/* Dropdown options */
div[data-baseweb="popover"],
div[data-baseweb="popover"] ul {
    background-color: #FFFFFF !important;
}

div[data-baseweb="popover"] li,
div[data-baseweb="popover"] li span {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    background-color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* Dropdown hover */
div[data-baseweb="popover"] li:hover {
    background-color: #DBEAFE !important;
}

/* ==========================================
   4. HEADINGS
========================================== */

h1, h2, h3 {
    color: #14213D !important;
    font-weight: 750 !important;
}

/* ==========================================
   5. KPI METRIC CARDS
========================================== */

div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    padding: 22px 20px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
    transition: all 0.25s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.12);
}

div[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-weight: 600 !important;
}

div[data-testid="stMetricValue"] {
    color: #163B65 !important;
    font-weight: 750 !important;
}

/* ==========================================
   6. CHARTS AND DATAFRAMES
========================================== */

div[data-testid="stPlotlyChart"],
div[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 10px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.05);
}

/* ==========================================
   7. INPUT FIELDS
========================================== */

div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    color: #172033 !important;
    background: #FFFFFF !important;
}

label {
    color: #334155 !important;
    font-weight: 600 !important;
}

/* ==========================================
   8. BUTTONS
========================================== */

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(
        90deg,
        #164E63,
        #0F9B8E
    ) !important;

    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px;
    font-weight: 650 !important;
    transition: 0.25s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(
        90deg,
        #0F766E,
        #14B8A6
    ) !important;

    color: #FFFFFF !important;
    box-shadow: 0 5px 15px rgba(15, 118, 110, 0.25);
}

/* ==========================================
   9. RADIO BUTTONS
========================================== */

div[role="radiogroup"] label {
    color: #FFFFFF !important;
}

/* ==========================================
   10. ALERTS
========================================== */

div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* ==========================================
   11. TABLES
========================================== */

[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

/* ==========================================
   12. FOOTER
========================================== */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)



# =====================================================
# 3. LOAD DATASET
# =====================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        "dataset/kmeans_clustered_results.csv"
    )


try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "Dataset not found! Check dataset/"
        "kmeans_clustered_results.csv"
    )

    st.stop()


required_columns = [
    "loan_amnt",
    "Default",
    "Cluster",
    "fico_n",
    "dti_n",
    "purpose",
    "emp_length"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        f"Missing columns: {missing_columns}"
    )

    st.stop()


df = df.copy()

for col in ["Default", "loan_amnt", "fico_n", "dti_n"]:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

df = df[
    df["Default"].isin([0, 1])
].copy()

if df.empty:
    st.error("No valid loan records found.")
    st.stop()


# =====================================================
# 4. SIDEBAR NAVIGATION
# =====================================================

st.sidebar.markdown(
    "## 💳 Credit Intelligence"
)

st.sidebar.caption(
    "LOAN PORTFOLIO ANALYTICS"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "📌 Dashboard Navigation",
    [
        "Portfolio Overview",
        "Cluster Analysis",
        "Credit Risk Analysis",
        "Business Insights",
        "Download Reports"
    ],
    key="main_navigation"
)

st.sidebar.divider()

st.sidebar.markdown(
    "### 🎛️ Portfolio Filters"
)

cluster_values = sorted(
    df["Cluster"].dropna().unique().tolist()
)

cluster_options = [
    "All Clusters"
] + cluster_values

selected_cluster = st.sidebar.selectbox(
    "Select K-Means Cluster",
    cluster_options,
    key="portfolio_cluster_filter"
)

if selected_cluster == "All Clusters":

    filtered_df = df.copy()

else:

    filtered_df = df[
        df["Cluster"] == selected_cluster
    ].copy()


st.sidebar.caption(
    f"Selected Loans: {len(filtered_df):,}"
)

st.sidebar.caption(
    f"Total Loans: {len(df):,}"
)

if filtered_df.empty:

    st.warning("No records found for this selection.")

    st.stop()


# =====================================================
# 5. COMMON FUNCTIONS
# =====================================================

def hero(title, description):

    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_kpis(data):

    total = len(data)

    avg_loan = data["loan_amnt"].mean()

    default_rate = (
        data["Default"].mean() * 100
    )

    clusters = data["Cluster"].nunique()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Loans",
        f"{total:,}"
    )

    c2.metric(
        "Average Loan",
        f"${avg_loan:,.2f}"
    )

    c3.metric(
        "Default Rate",
        f"{default_rate:.2f}%"
    )

    c4.metric(
        "Total Clusters",
        clusters
    )


def risk_table(data, column):

    result = (
        data.groupby(column, dropna=False)
        .agg(
            Total_Loans=("Default", "count"),
            Defaulted_Loans=("Default", "sum"),
            Default_Rate=("Default", "mean")
        )
        .reset_index()
    )

    result["Default_Rate"] *= 100

    return result.sort_values(
        "Default_Rate",
        ascending=False
    )


PLOT_STYLE = {
    "template": "plotly_white",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(255,255,255,0.8)",
    "font": {
        "family": "Arial",
        "color": "#263858"
    }
}


# =====================================================
# 6. PORTFOLIO OVERVIEW
# =====================================================

# =====================================================
# 6. PORTFOLIO OVERVIEW
# =====================================================

if page == "Portfolio Overview":

    # Page Header
    hero(
        "💳 Credit Portfolio Overview",
        "Monitor loan portfolio performance and historical credit risk."
    )

    # IMPORTANT: Use complete dataset, not filtered_df
    show_kpis(df)

    st.divider()

    # Two-column chart layout
    col1, col2 = st.columns(2)

    # =================================================
    # LOAN DISTRIBUTION BY CLUSTER
    # =================================================

    with col1:

        st.subheader(
            "📊 Loan Distribution by Cluster"
        )

        cluster_counts = (
            df["Cluster"]
            .value_counts()
            .sort_index()
            .rename_axis("Cluster")
            .reset_index(name="Loan Count")
        )

        fig = px.pie(
            cluster_counts,
            names="Cluster",
            values="Loan Count",
            hole=0.55,
            color="Cluster",
            color_discrete_sequence=(
                px.colors.qualitative.Bold
            )
        )

        fig.update_traces(
            textinfo="percent+label",
            textposition="inside"
        )

        fig.update_layout(
            **PLOT_STYLE,
            title="Loan Distribution Across 4 Clusters",
            showlegend=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =================================================
    # DEFAULT VS NON-DEFAULT
    # =================================================

    with col2:

        st.subheader(
            "⚠️ Default vs Non-default"
        )

        default_counts = (
            df["Default"]
            .value_counts()
            .reindex([0, 1], fill_value=0)
            .rename({
                0: "Non-default",
                1: "Default"
            })
            .rename_axis("Loan Status")
            .reset_index(name="Loan Count")
        )

        fig = px.pie(
            default_counts,
            names="Loan Status",
            values="Loan Count",
            hole=0.55,
            color="Loan Status",
            color_discrete_map={
                "Non-default": "#16A6A3",
                "Default": "#F05D5E"
            }
        )

        fig.update_traces(
            textinfo="percent+label",
            textposition="inside"
        )

        fig.update_layout(
            **PLOT_STYLE,
            title="Overall Default Distribution",
            showlegend=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # =================================================
    # COMPLETE CLUSTER PORTFOLIO SUMMARY
    # =================================================

    st.subheader(
        "📌 Cluster Portfolio Summary"
    )

    summary = (
        df.groupby("Cluster")
        .agg(
            Loan_Count=("Default", "size"),
            Average_Loan_Amount=("loan_amnt", "mean"),
            Average_FICO=("fico_n", "mean"),
            Average_DTI=("dti_n", "mean"),
            Default_Rate=("Default", "mean")
        )
        .reset_index()
    )

    summary["Default_Rate"] *= 100

    st.dataframe(
        summary.round(2),
        use_container_width=True,
        hide_index=True
    )



# =====================================================
# 7. CLUSTER ANALYSIS
# =====================================================

elif page == "Cluster Analysis":

    hero(
        "🎯 K-Means Cluster Analysis",
        "Explore borrower segments and compare their financial profiles."
    )

    show_kpis(filtered_df)

    st.divider()

    cluster_counts = (
        filtered_df["Cluster"]
        .value_counts()
        .sort_index()
        .rename_axis("Cluster")
        .reset_index(name="Loan Count")
    )

    st.subheader(
        "Cluster Distribution"
    )

    fig = px.bar(
        cluster_counts,
        x="Cluster",
        y="Loan Count",
        color="Cluster",
        text="Loan Count",
        color_discrete_sequence=(
            px.colors.qualitative.Bold
        ),
        title="Number of Loans in Each Cluster"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(**PLOT_STYLE)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Cluster Financial Profile"
    )

    profile = (
        filtered_df.groupby("Cluster")
        .agg(
            Loan_Count=("Default", "size"),
            Average_Revenue=(
                "revenue",
                "mean"
            ) if "revenue" in filtered_df.columns
            else ("loan_amnt", "mean"),
            Average_Loan_Amount=("loan_amnt", "mean"),
            Average_FICO=("fico_n", "mean"),
            Average_DTI=("dti_n", "mean"),
            Default_Rate=("Default", "mean")
        )
        .reset_index()
    )

    profile["Default_Rate"] *= 100

    st.dataframe(
        profile.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "⚠️ Default Rate by Cluster"
    )

    cluster_risk = risk_table(
        filtered_df,
        "Cluster"
    )

    fig = px.bar(
        cluster_risk,
        x="Cluster",
        y="Default_Rate",
        color="Default_Rate",
        text=cluster_risk["Default_Rate"].map(
            lambda x: f"{x:.2f}%"
        ),
        color_continuous_scale=[
            "#16A6A3",
            "#F6B44B",
            "#E55353"
        ]
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(**PLOT_STYLE)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# 8. CREDIT RISK ANALYSIS
# =====================================================

elif page == "Credit Risk Analysis":

    hero(
        "⚠️ Credit Risk Analysis",
        "Understand historical default patterns across borrower characteristics."
    )

    show_kpis(filtered_df)

    st.divider()

    # FICO ANALYSIS

    st.subheader(
        "📉 FICO Score vs Default Risk"
    )

    fico_bins = [
        float("-inf"),
        600,
        650,
        700,
        750,
        800,
        float("inf")
    ]

    fico_labels = [
        "Below 600",
        "600–650",
        "650–700",
        "700–750",
        "750–800",
        "800+"
    ]

    fico_group = pd.cut(
        filtered_df["fico_n"],
        bins=fico_bins,
        labels=fico_labels,
        right=False
    )

    fico_risk = (
        filtered_df.assign(
            FICO_Group=fico_group
        )
        .groupby(
            "FICO_Group",
            observed=False
        )["Default"]
        .mean()
        .mul(100)
        .reset_index(
            name="Default Rate"
        )
    )

    fig = px.bar(
        fico_risk,
        x="FICO_Group",
        y="Default Rate",
        color="Default Rate",
        text=fico_risk["Default Rate"].map(
            lambda x: f"{x:.2f}%"
        ),
        color_continuous_scale="Teal"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(**PLOT_STYLE)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # DTI ANALYSIS

    st.subheader(
        "📊 Debt-to-Income Ratio vs Default Risk"
    )

    dti_bins = [
        float("-inf"),
        10,
        20,
        30,
        40,
        float("inf")
    ]

    dti_labels = [
        "Below 10",
        "10–20",
        "20–30",
        "30–40",
        "40+"
    ]

    dti_group = pd.cut(
        filtered_df["dti_n"],
        bins=dti_bins,
        labels=dti_labels,
        right=False
    )

    dti_risk = (
        filtered_df.assign(
            DTI_Group=dti_group
        )
        .groupby(
            "DTI_Group",
            observed=False
        )["Default"]
        .mean()
        .mul(100)
        .reset_index(
            name="Default Rate"
        )
    )

    fig = px.bar(
        dti_risk,
        x="DTI_Group",
        y="Default Rate",
        color="Default Rate",
        text=dti_risk["Default Rate"].map(
            lambda x: f"{x:.2f}%"
        ),
        color_continuous_scale="Sunset"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(**PLOT_STYLE)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    col1, col2 = st.columns(2)

    # LOAN PURPOSE

    with col1:

        st.subheader(
            "🎯 Loan Purpose Risk"
        )

        purpose_risk = risk_table(
            filtered_df,
            "purpose"
        )

        fig = px.bar(
            purpose_risk.sort_values(
                "Default_Rate"
            ),
            x="Default_Rate",
            y="purpose",
            orientation="h",
            color="Default_Rate",
            color_continuous_scale="Tealgrn"
        )

        fig.update_layout(**PLOT_STYLE)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # EMPLOYMENT

    with col2:

        st.subheader(
            "👩‍💼 Employment Risk"
        )

        employment_risk = risk_table(
            filtered_df,
            "emp_length"
        )

        fig = px.bar(
            employment_risk.sort_values(
                "Default_Rate"
            ),
            x="Default_Rate",
            y="emp_length",
            orientation="h",
            color="Default_Rate",
            color_continuous_scale="Agsunset"
        )

        fig.update_layout(**PLOT_STYLE)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.caption(
        "These are historical associations. Small groups may have "
        "unstable rates. They do not establish causation."
    )


# =====================================================
# 9. BUSINESS INSIGHTS
# =====================================================

elif page == "Business Insights":

    hero(
        "💡 Business Insights & Recommendations",
        "Translate portfolio analysis into practical monitoring priorities."
    )

    show_kpis(filtered_df)

    st.divider()

    full_risk = risk_table(
        df,
        "Cluster"
    )

    highest = full_risk.iloc[0]
    lowest = full_risk.iloc[-1]

    col1, col2 = st.columns(2)

    col1.metric(
        "Highest Default Risk",
        f"Cluster {int(highest['Cluster'])}",
        f"{highest['Default_Rate']:.2f}%"
    )

    col2.metric(
        "Lowest Default Risk",
        f"Cluster {int(lowest['Cluster'])}",
        f"{lowest['Default_Rate']:.2f}%"
    )

    st.divider()

    st.subheader(
        "📌 Key Findings"
    )

    st.info(
        "Clusters have different borrower and financial characteristics. "
        "Comparing their default rates helps identify segments that may "
        "need closer monitoring."
    )

    st.warning(
        "Higher DTI groups show higher historical default rates in "
        "this dataset."
    )

    st.success(
        "Higher FICO score groups generally show lower historical "
        "default rates in this dataset."
    )

    st.subheader(
        "🚀 Business Recommendations"
    )

    rec1, rec2 = st.columns(2)

    with rec1:

        st.info(
            "**Portfolio Monitoring**\n\n"
            "Monitor segments with higher observed default rates."
        )

        st.info(
            "**Borrower Assessment**\n\n"
            "Consider FICO and DTI together when reviewing risk."
        )

    with rec2:

        st.warning(
            "**Data Quality**\n\n"
            "Check missing values, unusual values and group sizes."
        )

        st.success(
            "**Model Validation**\n\n"
            "Validate historical patterns using new data before "
            "operational use."
        )

    st.caption(
        "These findings are descriptive, not causal conclusions "
        "or a validated credit decision model."
    )


# =====================================================
# 10. DOWNLOAD REPORTS
# =====================================================

elif page == "Download Reports":

    hero(
        "📥 Download Portfolio Reports",
        "Export filtered loan records and cluster summaries."
    )

    show_kpis(filtered_df)

    st.divider()

    st.subheader(
        "Download Loan Dataset"
    )

    csv_data = (
        filtered_df.to_csv(
            index=False
        ).encode("utf-8")
    )

    st.download_button(
        label="⬇️ Download Filtered Loan Data",
        data=csv_data,
        file_name="credit_portfolio_filtered_data.csv",
        mime="text/csv",
        key="download_loans"
    )

    st.divider()

    st.subheader(
        "Download Cluster Summary"
    )

    summary = (
        filtered_df.groupby("Cluster")
        .agg(
            Loan_Count=("Default", "size"),
            Average_Loan_Amount=("loan_amnt", "mean"),
            Average_FICO=("fico_n", "mean"),
            Average_DTI=("dti_n", "mean"),
            Default_Rate=("Default", "mean")
        )
        .reset_index()
    )

    summary["Default_Rate"] *= 100

    summary_csv = (
        summary.to_csv(
            index=False
        ).encode("utf-8")
    )

    st.download_button(
        label="⬇️ Download Cluster Summary",
        data=summary_csv,
        file_name="credit_cluster_summary.csv",
        mime="text/csv",
        key="download_summary"
    )

    st.subheader(
        "📊 Cluster Summary Preview"
    )

    st.dataframe(
        summary.round(2),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# 11. FOOTER
# =====================================================

st.sidebar.divider()

st.sidebar.caption(
    "💳 Credit Portfolio Segmentation"
)

st.sidebar.caption(
    "Machine Learning | Risk Analytics"
)

st.markdown("---")

st.caption(
    "Credit Portfolio Segmentation & Risk Analysis | "
    "Interactive Streamlit Dashboard"
)
