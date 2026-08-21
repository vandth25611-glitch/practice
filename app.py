import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Practice 5 - Big Data Benchmark",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Practice 5 — Online Retail Big Data Benchmark")
st.caption("Performance comparison of Big Data processing tools on Online Retail Parquet")

CSV_FILE = "bigdata_parquet_benchmark_results.csv"

if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    st.success("Benchmark results loaded from repository.")
else:
    st.info("Upload the benchmark CSV below to display your final results.")
    uploaded = st.file_uploader(
        "Upload bigdata_parquet_benchmark_results.csv",
        type=["csv"]
    )
    if uploaded is None:
        st.markdown("""
        ### Required benchmark
        The final benchmark should contain:
        **Pandas, Polars, DuckDB, Dask, Vaex, PySpark and Ray Data**.

        After uploading the CSV, the dashboard will show the ranking,
        execution time and speedup versus Pandas.
        """)
        st.stop()
    df = pd.read_csv(uploaded)

st.subheader("🏆 Benchmark Ranking")

if "Rank" in df.columns:
    display_cols = [
        c for c in [
            "Rank", "Tool", "Median_s",
            "Mean_s", "Std_s", "Speedup_vs_Pandas_x"
        ] if c in df.columns
    ]
    st.dataframe(
        df[display_cols],
        use_container_width=True,
        hide_index=True
    )
else:
    st.dataframe(df, use_container_width=True, hide_index=True)

if "Tool" in df.columns and "Median_s" in df.columns:
    chart_df = df[["Tool", "Median_s"]].dropna().sort_values("Median_s")
    st.subheader("⏱️ Median Execution Time")
    st.bar_chart(chart_df.set_index("Tool"))

    winner = chart_df.iloc[0]
    st.metric(
        "Fastest Tool",
        winner["Tool"],
        f"{winner['Median_s']:.4f} seconds"
    )

if "Speedup_vs_Pandas_x" in df.columns:
    st.subheader("⚡ Speedup vs Pandas")
    speed_df = df[["Tool", "Speedup_vs_Pandas_x"]].dropna()
    st.bar_chart(speed_df.set_index("Tool"))

st.subheader("📥 Download Results")
st.download_button(
    "Download benchmark CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="bigdata_parquet_benchmark_results.csv",
    mime="text/csv"
)

st.divider()
st.caption("Practice 5 | Online Retail | Big Data Performance Benchmark")
