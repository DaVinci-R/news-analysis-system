import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from datetime import datetime, date
import re
from collections import Counter

# 页面配置
st.set_page_config(
    page_title="新闻分析报告",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 数据库连接
@st.cache_resource
def init_connection():
    """初始化数据库连接"""
    engine = create_engine('mysql+pymysql://root:qwer123123@localhost/cls_news_db')
    return engine


@st.cache_data
def load_data(selected_date, selected_categories):
    """加载数据"""
    engine = init_connection()

    # 构建SQL查询
    date_condition = f"date = '{selected_date}'"

    if "全部" not in selected_categories:
        category_list = "', '".join(selected_categories)
        category_condition = f" AND category IN ('{category_list}')"
    else:
        category_condition = ""

    # 查询analysis_results表
    analysis_query = f"""
    SELECT date, category, is_market_relevant, keywords, sentiment, impact_markets
    FROM analysis_results 
    WHERE {date_condition}{category_condition}
    """

    # 查询summary表
    summary_query = f"""
    SELECT date, category, summary
    FROM summary 
    WHERE {date_condition}{category_condition}
    """

    try:
        analysis_df = pd.read_sql(analysis_query, engine)
        summary_df = pd.read_sql(summary_query, engine)
        return analysis_df, summary_df
    except Exception as e:
        st.error(f"数据加载失败: {e}")
        return pd.DataFrame(), pd.DataFrame()


def get_available_dates():
    """获取可用的日期列表"""
    engine = init_connection()
    query = "SELECT DISTINCT date FROM analysis_results ORDER BY date DESC"
    try:
        dates_df = pd.read_sql(query, engine)
        return dates_df['date'].tolist()
    except:
        return []


def get_available_categories():
    """获取可用的类别列表"""
    engine = init_connection()
    query = "SELECT DISTINCT category FROM analysis_results ORDER BY category"
    try:
        categories_df = pd.read_sql(query, engine)
        return categories_df['category'].tolist()
    except:
        return []


def parse_keywords(keywords_series):
    """解析关键词字符串，统计频率"""
    all_keywords = []
    for keywords_str in keywords_series.dropna():
        if isinstance(keywords_str, str):
            # 假设关键词以逗号分隔
            keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
            all_keywords.extend(keywords)

    # 统计频率并返回前10
    keyword_counts = Counter(all_keywords)
    return keyword_counts.most_common(10)


def parse_impact_markets(markets_series):
    """解析影响市场字符串，统计频率"""
    all_markets = []
    for markets_str in markets_series.dropna():
        if isinstance(markets_str, str):
            # 假设市场以逗号分隔
            markets = [market.strip() for market in markets_str.split(',') if market.strip()]
            all_markets.extend(markets)

    # 统计频率并返回前10
    market_counts = Counter(all_markets)
    return market_counts.most_common(10)


def create_market_relevance_pie(df):
    """创建市场相关性饼图"""
    if df.empty:
        return go.Figure()

    relevance_counts = df['is_market_relevant'].value_counts()
    labels = ['相关' if x == 1 else '不相关' for x in relevance_counts.index]

    fig = px.pie(
        values=relevance_counts.values,
        names=labels,
        title="新闻市场相关性分布",
        color_discrete_map={'相关': '#2E8B57', '不相关': '#DC143C'}
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def create_keywords_bar(df):
    """创建关键词柱状图"""
    if df.empty:
        return go.Figure()

    top_keywords = parse_keywords(df['keywords'])

    if not top_keywords:
        return go.Figure()

    keywords, counts = zip(*top_keywords)

    fig = px.bar(
        x=list(counts),
        y=list(keywords),
        orientation='h',
        title="热门关键词 Top 10",
        labels={'x': '出现次数', 'y': '关键词'}
    )

    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig


def create_sentiment_analysis(df):
    """创建情绪分析图表"""
    if df.empty:
        return go.Figure(), 0

    # 整体平均情绪
    overall_sentiment = df['sentiment'].mean()

    # 各类别平均情绪
    category_sentiment = df.groupby('category')['sentiment'].mean().reset_index()

    fig = px.bar(
        category_sentiment,
        x='category',
        y='sentiment',
        title="各类别新闻情绪指标",
        labels={'sentiment': '平均情绪值', 'category': '新闻类别'}
    )

    # 添加整体平均线
    fig.add_hline(y=overall_sentiment, line_dash="dash",
                  annotation_text=f"整体平均: {overall_sentiment:.2f}")

    return fig, overall_sentiment


def create_impact_markets_chart(df):
    """创建影响市场图表"""
    if df.empty:
        return go.Figure()

    top_markets = parse_impact_markets(df['impact_markets'])

    if not top_markets:
        return go.Figure()

    markets, counts = zip(*top_markets)

    fig = px.bar(
        x=list(markets),
        y=list(counts),
        title="受影响市场 Top 10",
        labels={'x': '市场', 'y': '提及次数'}
    )

    fig.update_xaxes(tickangle=45)
    return fig


# 主界面
def main():
    st.title("📊 新闻分析报告可视化系统")
    st.markdown("---")

    # 侧边栏 - 筛选器
    st.sidebar.header("📅 筛选设置")

    # 获取可用日期和类别
    available_dates = get_available_dates()
    available_categories = get_available_categories()

    if not available_dates:
        st.error("无法获取数据库中的日期信息，请检查数据库连接。")
        return

    # 日期选择
    selected_date = st.sidebar.selectbox(
        "选择日期",
        options=available_dates,
        index=0
    )

    # 类别选择
    category_options = ["全部"] + available_categories
    selected_categories = st.sidebar.multiselect(
        "选择新闻类别",
        options=category_options,
        default=["全部"]
    )

    # 加载数据
    with st.spinner("正在加载数据..."):
        analysis_df, summary_df = load_data(selected_date, selected_categories)

    if analysis_df.empty:
        st.warning("所选条件下没有找到数据。")
        return

    # 显示数据概览
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("新闻总数", len(analysis_df))
    with col2:
        market_relevant = len(analysis_df[analysis_df['is_market_relevant'] == 1])
        st.metric("市场相关新闻", market_relevant)
    with col3:
        st.metric("新闻类别数", analysis_df['category'].nunique())
    with col4:
        avg_sentiment = analysis_df['sentiment'].mean()
        st.metric("整体情绪指标", f"{avg_sentiment:.2f}")

    st.markdown("---")

    # 第一行：市场相关性饼图 + 情绪分析
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🥧 市场相关性分析")
        pie_fig = create_market_relevance_pie(analysis_df)
        st.plotly_chart(pie_fig, use_container_width=True)

    with col2:
        st.subheader("😊 各类别情绪分析")
        sentiment_fig, overall_sentiment = create_sentiment_analysis(analysis_df)
        st.plotly_chart(sentiment_fig, use_container_width=True)

    # 第二行：关键词分析 + 影响市场分析
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 热门关键词")
        keywords_fig = create_keywords_bar(analysis_df)
        st.plotly_chart(keywords_fig, use_container_width=True)

    with col2:
        st.subheader("📈 受影响市场")
        markets_fig = create_impact_markets_chart(analysis_df)
        st.plotly_chart(markets_fig, use_container_width=True)

    # 第三行：新闻总结
    st.markdown("---")
    st.subheader("📰 新闻总结")

    if not summary_df.empty:
        for _, row in summary_df.iterrows():
            with st.expander(f"📋 {row['category']} - {row['date']}"):
                st.write(row['summary'])
    else:
        st.info("所选条件下没有找到新闻总结数据。")


if __name__ == "__main__":
    main()