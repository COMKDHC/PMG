import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import sys
sys.path.append("../productmatchguide_log_dashboard/")

from utils import data_formatter


def main():
    # parsed_data = data_formatter.read_log_file("logs//single_search.log")
    # log_df = data_formatter.reformat_to_df(parsed_data)
    log_df = data_formatter.merge_and_reformat_logs()
    date_filtered_log = set_date_range(log_df=log_df)

    # item not converted(변환되지 않은 제품) 또는
    # Country Unknown(국가를 특정할 수 없는 IP) 제외할 수 있는 옵션
    date_filtered_log = set_options(log_df=date_filtered_log)

    col_1, col_2 = st.columns(2)

    with col_1:
        plot_pie_daily_search_count_by_validity(log_df=date_filtered_log)
    with col_2:
        plot_line_daily_search_count_by_validity(log_df=date_filtered_log)

    # 국가 (country) ---------------------------------------------------------------------
    color_group = set_color_group(
        log_df=date_filtered_log,
        col="country",
        colors=[
            px.colors.qualitative.Alphabet,
            px.colors.qualitative.Antique,
            px.colors.qualitative.Bold,
            px.colors.qualitative.D3,
            px.colors.qualitative.Dark24,
        ],
    )
    col_1, col_2 = st.columns(2)
    with col_1:
        st.subheader("Country")
        plot_pie_chart(
            log_df=date_filtered_log,
            col="country",
            title="Ratio",
            color_group=color_group,
        )
    with col_2:
        st.subheader("\n\n\n\n")
        plot_line_daily_count(
            log_df=date_filtered_log,
            col="country",
            title="Daily Count",
            color_group=color_group,
        )

    # 인증 (cert) ------------------------------------------------------------------------
    color_group = set_color_group(
        log_df=date_filtered_log,
        col="cert",
        colors=[px.colors.qualitative.Set3],
    )
    col_1, col_2 = st.columns(2)
    with col_1:
        st.subheader("Certification")
        plot_pie_chart(
            log_df=date_filtered_log,
            col="cert",
            title="Ratio",
            color_group=color_group,
        )
    with col_2:
        st.subheader("\n\n\n\n")
        plot_line_daily_count(
            log_df=date_filtered_log,
            col="cert",
            title="Daily Count",
            color_group=color_group,
        )

    # SPG ------------------------------------------------------------------------------
    color_group = set_color_group(
        log_df=date_filtered_log,
        col="spg",
        colors=[px.colors.qualitative.Set2],
    )
    col_1, col_2 = st.columns(2)
    with col_1:
        st.subheader("SPG")
        plot_pie_chart(
            log_df=date_filtered_log,
            col="spg",
            title="Ratio",
            color_group=color_group,
        )
    with col_2:
        st.subheader("\n\n\n\n")
        plot_line_daily_count(
            log_df=date_filtered_log,
            col="spg",
            title="Daily Count",
            color_group=color_group,
        )

    # 제조사 (manufac) --------------------------------------------------------------------
    color_group = set_color_group(
        log_df=date_filtered_log,
        col="manufac",
        colors=[px.colors.qualitative.G10],
    )
    col_1, col_2 = st.columns(2)
    with col_1:
        st.subheader("Competitor")
        plot_pie_chart(
            log_df=date_filtered_log,
            col="manufac",
            title="Ratio",
            color_group=color_group,
        )
    with col_2:
        st.subheader("\n\n\n\n")
        plot_line_daily_count(
            log_df=date_filtered_log,
            col="manufac",
            title="Daily Count",
            color_group=color_group,
        )

    # item desc --------------------------------------------------------------------
    # Calculate the value counts
    # Sort the value counts in descending order
    # value_counts = date_filtered_log["item_desc"].value_counts()
    # sorted_value_counts = value_counts.sort_values(ascending=False)

    value_counts = date_filtered_log.groupby("item_desc").size().reset_index(name="counts")
    merged_value_counts = pd.merge(date_filtered_log, value_counts, on="item_desc", how="left")
    merged_value_counts = merged_value_counts.sort_values(by=["counts", "spg"], ascending=[False, True])
    merged_value_counts = merged_value_counts.drop_duplicates(subset="item_desc")

    sorted_value_counts = merged_value_counts[["item_desc", "counts", "cert", "spg", "manufac"]]
    # .sort_values(by="counts", ascending=False)

    # Display the sorted value counts
    # st.write(f'### Counts of unique values in column `{column}`')
    st.write(sorted_value_counts)


    value_counts_cert = date_filtered_log["cert"].value_counts().sort_values(ascending=False)
    value_counts_spg = date_filtered_log["spg"].value_counts().sort_values(ascending=False)
    value_counts_manufac = date_filtered_log["manufac"].value_counts().sort_values(ascending=False)
    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        st.write(value_counts_cert)
    with col_2:
        st.write(value_counts_spg)
    with col_3:
        st.write(value_counts_manufac)

# TODO: 그래프 색상 통일하기

# safe line ===============================================================


def set_date_range(log_df: pd.DataFrame) -> tuple:
    first_date = log_df["date"].min()
    last_date = log_df["date"].max()

    selected_date_start, selected_date_end = st.select_slider(
        "Select date range",
        options=log_df["date"],
        value=(first_date, last_date)
    )

    # col1, col2 = st.columns(2)
    # with col1:
    #     selected_date_start = st.date_input(
    #         label="시작일",
    #         min_value=first_date,
    #         max_value=last_date,
    #         value=first_date,
    #     )
    # with col2:
    #     selected_date_end = st.date_input(
    #         label="종료일",
    #         min_value=first_date,
    #         max_value=last_date,
    #         value=last_date,
    #     )

    date_filtered_log = log_df[
        (log_df["date"] >= selected_date_start) & (log_df["date"] <= selected_date_end)
    ]

    return date_filtered_log


def set_options(log_df: pd.DataFrame):

    with st.sidebar:
        exclude_not_converted = st.toggle("변환되지 않은 데이터 제외")
        if exclude_not_converted:
            df = log_df[log_df["validity"] != "item not converted"]
        else:
            df = log_df

        exclude_country_unknown = st.toggle("비식별 국가 제외")
        if exclude_country_unknown:
            df_result = df[df["country"] != "Country Unknown"]
        else:
            df_result = df

        certification_option = st.multiselect("Select certification (optional)", log_df["cert"].unique(), log_df["cert"].unique())
        manufacturer_option = st.multiselect("Select competitor (optional)", log_df["manufac"].unique(), log_df["manufac"].unique())
        spg_option = st.multiselect("Select SPG (optional)", log_df["spg"].unique(), log_df["spg"].unique())
        country_option = st.multiselect("Select country (optional)", log_df["country"].unique(), log_df["country"].unique())

    df_result = df_result[df_result["cert"].isin(certification_option)]
    df_result = df_result[df_result["manufac"].isin(manufacturer_option)]
    df_result = df_result[df_result["spg"].isin(spg_option)]
    df_result = df_result[df_result["country"].isin(country_option)]

    return df_result


def plot_line_daily_search_count_by_validity(log_df):

    # 'date'와 'validity' 기준으로 그룹화하고 카운트 집계
    daily_counts = log_df.groupby(["date", "validity"]).size().unstack(fill_value=0)
    # Plotly 그래프 객체 생성
    fig = go.Figure()
    # 'item not converted' 데이터에 대한 채워진 영역 추가
    if "item not converted" in daily_counts.columns:
        fig.add_trace(
            go.Scatter(
                x=daily_counts.index,
                y=daily_counts["item not converted"],
                mode="lines",
                line=dict(width=3, color="rgb(231, 107, 243)"),
                name="item not converted",
            )
        )

    # 'item converted' 데이터에 대한 채워진 영역 추가
    if "item converted" in daily_counts.columns:
        fig.add_trace(
            go.Scatter(
                x=daily_counts.index,
                y=daily_counts["item converted"],
                mode="lines",
                line=dict(width=3, color="rgb(111, 231, 219)"),
                name="item converted",
            )
        )

    daily_counts = (
        log_df.value_counts("date").reset_index().sort_values(by=["date"], axis=0)
    )
    fig.add_trace(
        go.Scatter(
            x=daily_counts["date"],
            y=daily_counts["count"],
            mode="lines",
            name="Total",
            line=dict(width=3, color="grey"),
            opacity=0.3,
        )
    )

    # 레이아웃 설정
    fig.update_layout(
        title="Daily Search Count by Conversion Status",
        xaxis_title="Date",
        yaxis_title="Count",
        showlegend=True,
        hovermode="x unified",
    )

    # Streamlit을 통해 차트를 표시
    st.plotly_chart(fig, use_container_width=True)


def plot_pie_daily_search_count_by_validity(log_df):
    status_counts = log_df["validity"].value_counts()
    status_counts = status_counts.reindex(
        ["item converted", "item not converted"], fill_value=0
    )

    # 파이 차트 생성
    fig = go.Figure(
        data=[
            go.Pie(
                labels=status_counts.index,  # 레이블로 'item converted', 'item not converted' 사용 # noqa
                values=status_counts.values,  # 값으로 빈도 사용
                textinfo="value+percent",
                hole=0.3,  # 도넛 차트 스타일
                marker=dict(colors=["rgb(111, 231, 219)", "rgb(231, 107, 243)"]),
            )
        ]
    )

    # 차트 레이아웃 설정
    fig.update_layout(title="Conversion Status Distribution")

    st.plotly_chart(fig, use_container_width=True)


def set_color_group(log_df: pd.DataFrame, col: str, colors: list):
    category = sorted(log_df[col].unique())
    color_group = dict(zip(category, [x for xs in colors for x in xs]))

    return color_group


def plot_line_daily_count(
    log_df: pd.DataFrame, col: str, title: str, color_group: dict
):
    daily_counts = log_df.groupby(["date", col]).size().unstack(fill_value=0)

    fig = go.Figure()

    for _col in daily_counts.columns:
        df_counts = daily_counts[[_col]]

        fig.add_trace(
            go.Scatter(
                x=df_counts.index,
                y=df_counts[_col],
                mode="lines",
                line=dict(width=3, color=color_group[_col]),
                name=f"{_col}",
            )
        )
    fig.update_layout(title=title, hovermode="x unified", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def plot_pie_chart(log_df: pd.DataFrame, col: str, title: str, color_group: dict):

    df_counts = log_df[col].value_counts()

    fig = go.Figure(
        data=[
            go.Pie(
                labels=df_counts.index,
                values=df_counts.values,
                textinfo="value+percent",
                hole=0.3,
                direction="clockwise",
                marker=dict(colors=[color_group[label] for label in df_counts.index]),
            )
        ]
    )

    # 레이아웃 설정
    fig.update_layout(title=title)

    # 플롯을 보여줌
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
