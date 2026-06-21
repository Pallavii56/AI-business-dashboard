import streamlit as st
import pandas as pd

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Business Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================
# STYLING
# =====================================

st.markdown("""
<style>

.main{
background:#F6F9FC;
}

.block-container{
padding-top:2rem;
padding-left:4rem;
padding-right:4rem;
}

/* KPI */

.kpi-card{
padding:30px;
border-radius:24px;
color:white;
box-shadow:0 12px 30px rgba(0,0,0,.12);
transition:.3s;
margin-bottom:20px;
}

.kpi-card:hover{
transform:translateY(-6px);
}

.rev{
background:linear-gradient(
135deg,
#0EA5E9,
#2563EB
);
}

.avg{
background:linear-gradient(
135deg,
#8B5CF6,
#6D28D9
);
}

.high{
background:linear-gradient(
135deg,
#10B981,
#047857
);
}

.low{
background:linear-gradient(
135deg,
#F97316,
#DC2626
);
}

.kpi-title{
font-size:16px;
opacity:.95;
}

.kpi-value{
font-size:40px;
font-weight:800;
margin-top:14px;
}

/* summary */

.summary{
padding:20px;
background:white;
border-radius:20px;
box-shadow:0 6px 18px rgba(0,0,0,.08);
text-align:center;
}

.summary-value{
font-size:36px;
font-weight:bold;
color:#2563EB;
}

.footer{
padding:40px;
text-align:center;
color:gray;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================

st.title("📊 AI Business Dashboard")
st.caption(
    "Upload • Analyze • Visualize"
)

# =====================================
# UPLOAD
# =====================================

uploaded = st.file_uploader(
    "Upload Business CSV",
    type=["csv"]
)

# =====================================
# MAIN
# =====================================

if uploaded:

    try:

        df = pd.read_csv(uploaded)

        st.success(
            "Business data uploaded successfully"
        )

        # ---------------------
        # PREVIEW
        # ---------------------

        with st.expander(
            "📁 Dataset Preview"
        ):

            st.dataframe(
                df,
                use_container_width=True
            )

        # ---------------------
        # NUMERIC
        # ---------------------

        numeric = df.select_dtypes(
            include="number"
        )

        if numeric.empty:

            st.warning(
                "No numeric columns found."
            )

            st.stop()

        revenue = numeric.columns[0]

        total = df[revenue].sum()

        avg = df[revenue].mean()

        highest = df[revenue].max()

        lowest = df[revenue].min()

        # ---------------------
        # KPI
        # ---------------------

        st.markdown(
            "## 📌 KPI Dashboard"
        )

        c1,c2,c3,c4 = st.columns(4)

        with c1:

            st.markdown(f"""
            <div class="kpi-card rev">
            <div class="kpi-title">
            💰 Total Revenue
            </div>

            <div class="kpi-value">
            ₹{total:,.0f}
            </div>

            </div>
            """,
            unsafe_allow_html=True)

        with c2:

            st.markdown(f"""
            <div class="kpi-card avg">
            <div class="kpi-title">
            📈 Average Revenue
            </div>

            <div class="kpi-value">
            ₹{avg:,.0f}
            </div>

            </div>
            """,
            unsafe_allow_html=True)

        with c3:

            st.markdown(f"""
            <div class="kpi-card high">
            <div class="kpi-title">
            🚀 Highest Revenue
            </div>

            <div class="kpi-value">
            ₹{highest:,.0f}
            </div>

            </div>
            """,
            unsafe_allow_html=True)

        with c4:

            st.markdown(f"""
            <div class="kpi-card low">
            <div class="kpi-title">
            📉 Lowest Revenue
            </div>

            <div class="kpi-value">
            ₹{lowest:,.0f}
            </div>

            </div>
            """,
            unsafe_allow_html=True)

        # ---------------------
        # SUMMARY
        # ---------------------

        st.markdown(
            "## 📋 Data Summary"
        )

        s1,s2,s3,s4 = st.columns(4)

        vals = [

            ("Rows",df.shape[0]),

            ("Columns",df.shape[1]),

            (
                "Missing",
                int(
                    df.isnull()
                    .sum()
                    .sum()
                )
            ),

            (
                "Numeric",
                len(
                    numeric.columns
                )
            )
        ]

        for col,(title,val) in zip(
            [s1,s2,s3,s4],
            vals
        ):

            with col:

                st.markdown(f"""
                <div class='summary'>

                <h4>{title}</h4>

                <div class='summary-value'>
                {val}
                </div>

                </div>
                """,
                unsafe_allow_html=True)

        # ---------------------
        # CATEGORY
        # ---------------------

        if "category" in df.columns:

            st.markdown(
                "## 🏆 Top 5 Categories"
            )

            grouped = (

                df.groupby(
                    "category"
                )[revenue]

                .sum()

                .sort_values(
                    ascending=False
                )

                .head(5)

            )

            st.bar_chart(
                grouped
            )

        # ---------------------
        # MONTH
        # ---------------------

        if "date" in df.columns:

            st.markdown(
                "## 📈 Monthly Trend"
            )

            df["date"] = pd.to_datetime(
                df["date"],
                errors="coerce"
            )

            trend = (

                df.groupby(

                    df[
                        "date"
                    ]

                    .dt.strftime(
                        "%b"
                    )

                )[revenue]

                .sum()

            )

            st.line_chart(
                trend
            )

        # ---------------------
        # DOWNLOAD
        # ---------------------

        st.markdown(
            "## ⬇ Export Report"
        )

        st.download_button(

            label=
            "Download Processed CSV",

            data=df.to_csv(
                index=False
            ),

            file_name=
            "business_report.csv",

            mime=
            "text/csv"
        )

        st.markdown("""
        <div class='footer'>
        Built with Streamlit
        </div>
        """,
        unsafe_allow_html=True)

    except Exception as e:

        st.error(
            str(e)
        )