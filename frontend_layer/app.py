import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys
import requests
import json

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from frontend_layer import config

# 页面设置
st.set_page_config(
    page_title="DaVinci News - 智能金融分析系统",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 样式美化 ---
st.markdown("""
    <style>
    /* 全局背景与字体 */
    .main {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    /* 卡片样式 */
    .metric-card {
        background-color: #1a1c24;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2d2e3a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #4a90e2;
    }
    /* 聊天气泡 */
    .chat-bubble {
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        max-width: 85%;
        line-height: 1.5;
        font-size: 1.05rem;
    }
    .user-bubble {
        background-color: #3d4455;
        color: #ffffff;
        margin-left: auto;
        border-bottom-right-radius: 2px;
        border: 1px solid #4e566a;
    }
    .ai-bubble {
        background-color: #233a5d;
        color: #f0f4f8;
        margin-right: auto;
        border-bottom-left-radius: 2px;
        border-left: 5px solid #4a90e2;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    }
    /* 摘要卡片 */
    .summary-card {
        background: linear-gradient(135deg, #262f3f 0%, #1a2332 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #4a90e2;
        margin-bottom: 20px;
        color: #e2e8f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .summary-card h3 {
        color: #4a90e2;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 数据加载函数 ---
@st.cache_data(ttl=60)
def load_news_data():
    try:
        engine = create_engine(config.get_db_url())
        query = f"SELECT * FROM {config.TABLE_NAME} ORDER BY create_time DESC"
        df = pd.read_sql(query, con=engine)
        if not df.empty:
            # 处理 MySQL Time 类型 (Read as Timedelta) 导致的报错
            # 我们将 publish_date 和 publish_time 合并
            def combine_date_time(row):
                if pd.isna(row['publish_date']) or pd.isna(row['publish_time']):
                    return row['create_time']
                # 如果 publish_time 是 timedelta，将其加到 date 上
                if isinstance(row['publish_time'], pd.Timedelta):
                    return pd.to_datetime(row['publish_date']) + row['publish_time']
                return row['create_time']

            df['full_publish_time'] = df.apply(combine_date_time, axis=1)
            df['processed_at'] = pd.to_datetime(df['processed_at'])
        return df
    except Exception as e:
        st.error(f"数据加载或处理失败: {e}")
        import traceback
        st.code(traceback.format_exc()) # 方便调试
        return pd.DataFrame()

@st.cache_data(ttl=60)
def load_summary_data():
    try:
        engine = create_engine(config.get_db_url())
        query = f"SELECT * FROM {config.SUMMARY_TABLE} ORDER BY created_at DESC"
        df = pd.read_sql(query, con=engine)
        return df
    except Exception as e:
        return pd.DataFrame()

# --- 侧边栏 ---
st.sidebar.image("https://img.icons8.com/fluent/96/000000/combo-chart.png", width=80)
st.sidebar.title("DaVinci News")
st.sidebar.caption("v2.0 智能金融决策系统")

menu = st.sidebar.radio("核心导览", ["📊 实时仪表板", "🧠 市场深度综述", "💬 智能 AI 助理"])

st.sidebar.divider()

# --- 全局时间筛选 (仅对仪表板和综述生效) ---
date_range = None
if menu in ["📊 实时仪表板", "🧠 市场深度综述"]:
    st.sidebar.subheader("📅 时间范围筛选")
    # 默认显示最近 7 天
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)
    
    date_range = st.sidebar.date_input(
        "选择起止日期",
        value=(seven_days_ago, today),
        max_value=today,
        help="筛选新闻的发布时间或总结的创建时间"
    )
    
    if len(date_range) != 2:
        st.sidebar.warning("请选择完整的起止日期")

st.sidebar.divider()

# --- 主界面逻辑 ---

if menu == "📊 实时仪表板":
    st.title("🚀 全球金融新闻实时监控")
    
    df = load_news_data()
    if df.empty:
        st.warning("暂无数据。请确保后端爬虫与处理模组已启动。")
    else:
        # 应用时间筛选
        if date_range and len(date_range) == 2:
            start_date, end_date = date_range
            # 转换为 datetime 以便比对 (包含结束当天)
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date) + timedelta(days=1)
            
            df = df[(df['full_publish_time'] >= start_dt) & (df['full_publish_time'] < end_dt)]

        if df.empty:
            st.info(f"在 {date_range[0]} 至 {date_range[1]} 期间暂无新闻数据。")
        else:
            # 顶部指标
            processed_df = df[df['processed_at'].notnull()]
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("入库新闻", len(df))
            with c2:
                st.metric("结构化分析", len(processed_df))
            with c3:
                avg_sentiment = processed_df['sentiment_score'].mean() if not processed_df.empty else 0
                color = "normal" if abs(avg_sentiment) < 0.2 else "inverse"
                st.metric("平均情绪", f"{avg_sentiment:.2f}", delta=f"{avg_sentiment:.2f}", delta_color=color)
            with c4:
                if not processed_df.empty:
                    hot_asset = processed_df['asset_class'].mode()[0]
                    st.metric("焦点资产", hot_asset)
                else:
                    st.metric("焦点资产", "N/A")

            # 布局
            t1, t2 = st.tabs(["📉 趋势与分布", "📄 数据明细记录"])
            
            with t1:
                col_l, col_r = st.columns([2, 1])
                with col_l:
                    st.subheader("💡 行业情绪离散度")
                    if not processed_df.empty:
                        fig = px.box(processed_df, x="sector", y="sentiment_score", color="sector", template="plotly_dark")
                        st.plotly_chart(fig, use_container_width=True)
                with col_r:
                    st.subheader("🧭 资产类别分布")
                    if not processed_df.empty:
                        fig_pie = px.sunburst(processed_df, path=['asset_class', 'event_type'], values='impact_weight', template="plotly_dark")
                        st.plotly_chart(fig_pie, use_container_width=True)
                
                if not processed_df.empty:
                    st.subheader("📈 情绪波段演变 (Timeline)")
                    fig_line = px.line(processed_df.sort_values('full_publish_time'), x='full_publish_time', y='sentiment_score', 
                                       color='asset_class', markers=True, template="plotly_dark", line_shape='spline')
                    st.plotly_chart(fig_line, use_container_width=True)

            with t2:
                st.dataframe(
                    df[['full_publish_time', 'title', 'asset_class', 'sector', 'sentiment_score', 'impact_weight']],
                    column_config={
                        "full_publish_time": st.column_config.DatetimeColumn("发布时间", format="MM-DD HH:mm"),
                        "sentiment_score": st.column_config.NumberColumn("情绪分", format="%.2f"),
                        "impact_weight": st.column_config.ProgressColumn("影响力", min_value=1, max_value=5)
                    },
                    use_container_width=True
                )

elif menu == "🧠 市场深度综述":
    st.title("🧬 资产维度 · 深度 AI 复盘")
    st.info("本模块展示由 LLM 对特定资产大类进行的时间窗口聚合总结。")
    
    sum_df = load_summary_data()
    if sum_df.empty:
        st.write("目前尚未生成任何聚合总结。")
    else:
        # 应用时间筛选
        if date_range and len(date_range) == 2:
            start_date, end_date = date_range
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date) + timedelta(days=1)
            
            # 统计窗口或创建时间符合即可
            sum_df = sum_df[
                ((pd.to_datetime(sum_df['window_start']) >= start_dt) & (pd.to_datetime(sum_df['window_start']) < end_dt)) |
                ((pd.to_datetime(sum_df['created_at']) >= start_dt) & (pd.to_datetime(sum_df['created_at']) < end_dt))
            ]

        if sum_df.empty:
            st.info(f"在 {date_range[0]} 至 {date_range[1]} 期间暂无 AI 聚合总结。")
        else:
            # 过滤器
            assets = ["全部"] + sorted(sum_df['asset_class'].unique().tolist())
            selected_asset = st.selectbox("筛选资产大类", assets)
            
            display_sum = sum_df if selected_asset == "全部" else sum_df[sum_df['asset_class'] == selected_asset]
            
            if display_sum.empty:
                st.info("该资产类别在当前时间范围内暂无总结。")
            else:
                for idx, row in display_sum.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div class="summary-card">
                            <h3 style='margin-top:0;'>{row['asset_class']} 市场综述</h3>
                            <p style='color: #94a3b8; font-size: 0.9em;'>统计窗口: {row['window_start']} 至 {row['window_end']} | 样本量: {row['news_count']} 篇</p>
                            <hr style='border-color: #334155;'>
                            <div style='font-size: 1.1em; line-height: 1.6;'>
                                {row['summary_text'].replace('\n', '<br>')}
                            </div>
                            <p style='text-align: right; color: #475569; font-size: 0.8em; margin-top: 15px;'>生成于: {row['created_at']}</p>
                        </div>
                        """, unsafe_allow_html=True)

elif menu == "💬 智能 AI 助理":
    st.title("🤖 DaVinci 金融助手")
    st.markdown("您可以询问关于特定资产、行业的问题，助理将自动查询实时数据库并为您总结。")
    
    # 初始化聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示聊天记录
    for message in st.session_state.messages:
        role_class = "user-bubble" if message["role"] == "user" else "ai-bubble"
        st.markdown(f"""
        <div class="chat-bubble {role_class}">
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)

    # 用户输入
    if prompt := st.chat_input("例如：总结一下今日黄金的新闻"):
        # 显示用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(f'<div class="chat-bubble user-bubble">{prompt}</div>', unsafe_allow_html=True)
        
        # 调用后端 API
        with st.spinner("AI 正在深度思考并查询数据库..."):
            try:
                response = requests.post(config.INTERACTIVE_API_URL, json={"user_input": prompt}, timeout=60)
                if response.status_code == 200:
                    answer = response.json().get("answer", "未能获取回答")
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.markdown(f'<div class="chat-bubble ai-bubble">{answer}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"API请求失败: {response.text}")
            except Exception as e:
                st.error(f"连接交互层失败: {e}")

# 刷新按钮
if st.sidebar.button("🔄 刷新全局数据"):
    st.cache_data.clear()
    st.rerun()