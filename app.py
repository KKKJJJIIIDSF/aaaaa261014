import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="제조 품질 현황 대시보드",
    page_icon="🏭",
    layout="wide",
)


def create_sample_data():
    data = [
        ["2026-10-01", "P001", "OK", "None", 0.98],
        ["2026-10-01", "P002", "NG", "Scratch", 0.91],
        ["2026-10-02", "P003", "OK", "None", 0.96],
        ["2026-10-02", "P004", "NG", "Crack", 0.88],
        ["2026-10-03", "P005", "OK", "None", 0.97],
        ["2026-10-03", "P006", "NG", "Dent", 0.85],
        ["2026-10-04", "P007", "OK", "None", 0.99],
        ["2026-10-04", "P008", "NG", "Scratch", 0.90],
        ["2026-10-05", "P009", "OK", "None", 0.95],
        ["2026-10-05", "P010", "OK", "None", 0.98],
        ["2026-10-06", "P011", "NG", "Crack", 0.87],
        ["2026-10-06", "P012", "OK", "None", 0.96],
        ["2026-10-07", "P013", "OK", "None", 0.99],
        ["2026-10-07", "P014", "NG", "Scratch", 0.92],
        ["2026-10-08", "P015", "OK", "None", 0.97],
        ["2026-10-08", "P016", "NG", "Dent", 0.86],
        ["2026-10-09", "P017", "OK", "None", 0.98],
        ["2026-10-09", "P018", "NG", "Crack", 0.89],
        ["2026-10-10", "P019", "OK", "None", 0.97],
        ["2026-10-10", "P020", "OK", "None", 0.99],
    ]

    columns = [
        "inspection_date",
        "product_id",
        "result",
        "defect_type",
        "confidence",
    ]

    df = pd.DataFrame(data, columns=columns)
    df["inspection_date"] = pd.to_datetime(df["inspection_date"])
    return df


st.title("🏭 제조 품질 현황 대시보드")
st.caption("AI 비전검사 PoC 준비를 위한 품질 데이터 모니터링")

st.sidebar.header("데이터 설정")

uploaded_file = st.sidebar.file_uploader(
    "CSV 파일 업로드",
    type=["csv"],
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("CSV 파일을 불러왔습니다.")
    except Exception as e:
        st.error(f"CSV 파일을 읽을 수 없습니다: {e}")
        st.stop()
else:
    df = create_sample_data()
    st.sidebar.info("현재 기본 샘플 데이터를 사용하고 있습니다.")

required_columns = [
    "inspection_date",
    "product_id",
    "result",
    "defect_type",
    "confidence",
]

missing_columns = [
    column for column in required_columns if column not in df.columns
]

if missing_columns:
    st.error(
        "CSV에 다음 필수 컬럼이 없습니다: "
        + ", ".join(missing_columns)
    )
    st.stop()

df["inspection_date"] = pd.to_datetime(
    df["inspection_date"],
    errors="coerce",
)
df = df.dropna(subset=["inspection_date"])

st.sidebar.header("필터")

min_date = df["inspection_date"].min().date()
max_date = df["inspection_date"].max().date()

date_range = st.sidebar.date_input(
    "검사 날짜",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

product_options = sorted(df["product_id"].dropna().unique())

selected_products = st.sidebar.multiselect(
    "제품",
    options=product_options,
    default=product_options,
)

selected_results = st.sidebar.multiselect(
    "검사 결과",
    options=["OK", "NG"],
    default=["OK", "NG"],
)

filtered_df = df.copy()

if len(date_range) == 2:
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

    filtered_df = filtered_df[
        (filtered_df["inspection_date"] >= start_date)
        & (filtered_df["inspection_date"] <= end_date)
    ]

filtered_df = filtered_df[
    filtered_df["product_id"].isin(selected_products)
]

filtered_df = filtered_df[
    filtered_df["result"].isin(selected_results)
]

total_count = len(filtered_df)
ok_count = (filtered_df["result"] == "OK").sum()
ng_count = (filtered_df["result"] == "NG").sum()

if total_count > 0:
    defect_rate = ng_count / total_count * 100
else:
    defect_rate = 0

st.subheader("품질 현황")

col1, col2, col3, col4 = st.columns(4)

col1.metric("전체 검사", f"{total_count:,}건")
col2.metric("정상", f"{ok_count:,}건")
col3.metric("불량", f"{ng_count:,}건")
col4.metric("불량률", f"{defect_rate:.1f}%")

st.divider()

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 날짜별 검사 현황")

    if not filtered_df.empty:
        daily_data = (
            filtered_df
            .groupby("inspection_date")
            .size()
            .rename("검사 건수")
        )
        st.line_chart(daily_data)
    else:
        st.info("표시할 데이터가 없습니다.")

with chart_col2:
    st.subheader("📊 불량 유형별 건수")

    defect_df = filtered_df[
        (filtered_df["result"] == "NG")
        & (filtered_df["defect_type"] != "None")
    ]

    if not defect_df.empty:
        defect_data = (
            defect_df
            .groupby("defect_type")
            .size()
            .rename("불량 건수")
            .sort_values(ascending=False)
        )
        st.bar_chart(defect_data)
    else:
        st.info("표시할 불량 데이터가 없습니다.")

st.divider()

st.subheader("🔎 최근 검사 결과")

if not filtered_df.empty:
    recent_df = (
        filtered_df
        .sort_values("inspection_date", ascending=False)
        .head(10)
        .copy()
    )

    recent_df["inspection_date"] = recent_df[
        "inspection_date"
    ].dt.strftime("%Y-%m-%d")

    recent_df = recent_df.rename(
        columns={
            "inspection_date": "검사일",
            "product_id": "제품 ID",
            "result": "검사 결과",
            "defect_type": "불량 유형",
            "confidence": "신뢰도",
        }
    )

    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("표시할 검사 결과가 없습니다.")

st.caption(f"현재 표시 중인 데이터: {len(filtered_df):,}건")
