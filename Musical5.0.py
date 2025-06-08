#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


# In[11]:


import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 应用配置
st.set_page_config(
    page_title="张沁丹六月演什么戏？",
    page_icon="🥚",
    layout="wide"
)

# 自定义CSS样式
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'STZhongsong', 'SimSun', serif;
    }
    
    .main {
        background-color: #ffffff;
    }
    
    /* 顶部横幅 */
    .header-image {
        width: 100%;
        height: 450px;
        object-fit: cover;
        margin-bottom: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* 轮播图样式 */
    .carousel {
        position: relative;
        width: 100%;
        height: 450px;
        overflow: hidden;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    .carousel-inner {
        display: flex;
        transition: transform 0.5s ease;
        height: 100%;
    }
    
    .carousel-item {
        min-width: 100%;
        height: 100%;
    }
    
    .carousel-item img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* 卡片样式 */
    .musical-card {
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #fff5f5;
        border-left: 5px solid #d23c3c;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .musical-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .musical-title {
        color: #8c1a1a;
        font-weight: bold;
        font-size: 1.5em;
        margin-bottom: 10px;
    }
    
    .theater-name {
        color: #d23c3c;
        font-weight: bold;
        font-size: 1.1em;
        margin: 8px 0;
    }
    
    /* 按钮样式 */
    .stButton>button {
        background-color: #d23c3c;
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
        border: none;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #991a1a;
        color: white;
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #fff0f0;
    }
    
    /* 选项卡样式 */
    [role="tab"] {
        font-weight: bold;
        color: #d23c3c;
        padding: 8px 16px;
    }
    
    [aria-selected="true"] {
        color: #8c1a1a !important;
        border-bottom: 3px solid #d23c3c;
    }
    
    /* 标题样式 */
    h1 {
        color: #8c1a1a !important;
        border-bottom: 2px solid #d23c3c;
        padding-bottom: 10px;
    }
    
    /* 表单样式 */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stDateInput>div>div>input,
    .stTimeInput>div>div>input {
        border: 1px solid #ffd0d0;
        border-radius: 4px;
    }
    
    /* 表格样式 */
    .stDataFrame {
        border: 1px solid #ffd0d0;
        border-radius: 8px;
    }
    
    /* 演员介绍卡片 */
    .actor-card {
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        background-color: #f8f8f8;
        border-left: 5px solid #8c1a1a;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    .actor-name {
        color: #8c1a1a;
        font-size: 1.8em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 顶部轮播图
header_images = [
    "https://i.imgur.com/KUOhkeq.jpeg",
    "https://i.imgur.com/3KAIyAH.jpeg"
]

st.markdown(f"""
<div class="carousel">
    <div class="carousel-inner" style="transform: translateX(-{st.session_state.get('carousel_pos', 0)}%);">
        {"".join([f'<div class="carousel-item"><img src="{img}"></div>' for img in header_images])}
    </div>
</div>
""", unsafe_allow_html=True)

if 'carousel_pos' not in st.session_state:
    st.session_state.carousel_pos = 0
    st.session_state.carousel_timer = 0

# 自动轮播逻辑
if st.session_state.carousel_timer >= 1:  # 每1秒切换一次
    st.session_state.carousel_pos = (st.session_state.carousel_pos + 100) % (len(header_images) * 100)
    st.session_state.carousel_timer = 0
    st.rerun()
else:
    st.session_state.carousel_timer += 1

# 加载音乐剧数据
@st.cache_data
def load_data():
    data = {
        "剧目名称": ["连璧", "谨遵医嘱", "TRACE U", "宝玉", "LIZZIE丽兹", "疯子与赞美诗"],
        "演出日期": ["2025-06-13", "2025-06-14", "2025-06-20", "2025-06-28", "2025-6-14", "2025-6-02"],
        "演出时间": ["19:30", "19:30", "14:00", "20:00", "14:00", "19:30"],
        "剧院名称": ["她剧场", "十一楼哪个剧场", "上海茉莉花剧场", "北京保利剧院", "大世界", "墨剧场"],
        "票价范围": ["280-1280元", "180-1080元", "200-880元", "380-1680元", "280-1280元", "180-980元"],
        "购票链接": [
            "https://mp.weixin.qq.com/s/TvkxIL5pU5s8Dv9tJz9sFg",
            "https://mp.weixin.qq.com/s/VKNxD1aHzpBcgHOTD3kYSw",
            "https://mp.weixin.qq.com/s/yqfXa9SummO5tS75v2PkAA",
            "https://mp.weixin.qq.com/s/5LfK_f-9I-tlgq3D-0kCDg",
            "https://mp.weixin.qq.com/s/64sbDcQmHDirJzDPpvvhDA",
            "https://www.dahepiao.com/news1/yanchu/20231031428269.html"
        ],
        "海报图片": [
            "https://i.imgur.com/So5kIsT.jpeg",
            "https://i.imgur.com/oe7bnsw.jpeg",
            "https://i.imgur.com/sxaHw9y.jpeg",
            "https://i.imgur.com/Giy1xkI.jpeg",
            "https://i.imgur.com/medYtwb.png",
            "https://i.imgur.com/peYTYbc.jpeg"
        ],
        "简介": [
            "在桉城一手遮天的李氏家族中，人人纸醉金迷、争权夺利。集团千金李玉屏与第一秘书谢宛宁，针锋相对水火不容。曾是挚友的她们，为何会反目成仇？勾心斗角的名利场上，她们能否得偿所愿？深不见底的命运漩涡中，她们又是否能够看清自己的内心？揭开尘封的往事，走进金丝的牢笼，秘密与羁绊的舞台，拉开帷幕。",
            "中年马拉松公益跑者马勤意外查出惠上阿尔兹海默症，生活急转而下，工作失利，家庭瓦解，他剩余的一半人生开始与倒退的记忆赛跑。他再度走访那些与自己生活相关的人，开启了一场独属自己的“去伪存真”，摆在他面前的，是人生的发令枪，拿起或放下，答案无人知晓..",
            "在一家名为“Debai”的摇滚酒吧中，主唱启夏和吉他手庭宇因为热爱摇滚而单纯地活着。然而，一名神秘女子的出现打乱了他们原本简单的生活，启夏对女子执着的追逐引发了他和庭宇之间接二连三的争执。随着两人矛盾的逐渐加深，隐藏在时间和记忆深处的真相慢慢显现了出来……",
            "音乐剧《宝玉》以《红楼梦》中“宝玉”的视角,重新解构和诠释这个故事。“宝玉”不仅指贾宝玉或通灵宝玉,更是一种身份与命运的象征。在戏中，宝玉是贾家的公子,也是天地间的顽石,他的命运似乎被提前写定。然而,这个少年在寻求自我答案的过程中,质疑预设的命运,感受并经历爱恨情仇,最终成为完整的“宝玉”。",
            "1892年8月4日，一个闷热夏日的午后，美国马塞诸塞州的福尔里弗，吝啬的银行家 AndrewJackson Borden 和他的第二任妻子 Abby 惨死于家中，Borden 先生的二女儿 Lizzie Andrew Borden成为了头号嫌疑人。Lizzie 的审判引起了轰动，也将Borden 家的女仆 BridgetLizzie 的姐姐 Emma,和邻居 Alice 卷入其中。",
            "刚出狱的李默在陌生的环境中无法融入社会，身体的饥饿和内心的怯懦让他备受煎熬，他突然开始怀念监狱里强规则的生活，所以李默打算重回他的安全区——监狱。但当他故意“犯罪”的时候，却遇到了与他想法截然相反，为了追求包由和梦想，相对安全的医院里逃离的疯子。在疯子的“哄骗”下，二人结伴而行，不知不觉中，李默也学会了疯子“精神胜利法”这一套理论,并将其付诸实践。"
        ]
    }
    df = pd.DataFrame(data)
    df["演出日期"] = pd.to_datetime(df["演出日期"])
    return df

df = load_data()

# 侧边栏 - 筛选条件
with st.sidebar:
    st.title("🎭 筛选条件")
    
    # 日期范围选择
    min_date = df["演出日期"].min().to_pydatetime()
    max_date = df["演出日期"].max().to_pydatetime()
    date_range = st.date_input(
        "选择日期范围",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # 剧院选择
    theaters = st.multiselect(
        "选择剧院",
        options=df["剧院名称"].unique(),
        default=df["剧院名称"].unique()
    )
    
    # 票价范围
    price_ranges = st.multiselect(
        "选择票价范围",
        options=df["票价范围"].unique(),
        default=df["票价范围"].unique()
    )
    
    # 排序方式
    sort_by = st.selectbox(
        "排序方式",
        options=["演出日期", "剧目名称", "剧院名称"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("**关于**")
    st.markdown("本应用提供张沁丹当月演出信息")

# 过滤数据
filtered_df = df[
    (df["演出日期"] >= pd.to_datetime(date_range[0])) &
    (df["演出日期"] <= pd.to_datetime(date_range[1])) &
    (df["剧院名称"].isin(theaters)) &
    (df["票价范围"].isin(price_ranges))
].sort_values(sort_by)

# 主页面
st.title("🥚张沁丹六月演什么戏？")
st.markdown("查看禽蛋🥚最新演出信息")

# 添加张沁丹介绍板块
with st.expander("🎭 关于张沁丹", expanded=True):
    st.markdown("""
    <div class="actor-card">
        <div class="actor-name">张沁丹</div>
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="flex: 0 0 200px;">
                <img src="https://i.imgur.com/LzIVhfL.jpeg" style="width: 100%; border-radius: 8px;">
            </div>
            <div style="flex: 1;">
                <p><strong>职业：</strong>音乐剧演员</p>
                <p><strong>代表作品：</strong>《人间失格》《伪装者2022》《猎罪图鉴》《道林格雷的画像》</p>
                <p><strong>简介：</strong>张沁丹是中国新生代音乐剧演员，以其扎实的唱功和富有感染力的表演风格受到观众喜爱。毕业于上海音乐学院音乐剧系，曾出演多部经典音乐剧作品，塑造了多个令人印象深刻的角色形象。</p>
                <p><strong>演出特点：</strong>声音清澈透亮，表演细腻真实，擅长塑造复杂多面的女性角色。</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 显示结果数量
st.markdown(f"**找到 {len(filtered_df)} 场演出**")

# 选项卡布局
tab1, tab2, tab3 = st.tabs(["卡片视图", "表格视图", "地图视图"])

with tab1:
    # 卡片视图
    if filtered_df.empty:
        st.warning("没有找到符合条件的演出")
    else:
        for idx, row in filtered_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="musical-card">
                    <div style="display: flex;">
                        <div style="flex: 1;">
                            <div class="musical-title">{row['剧目名称']}</div>
                            <div><strong>演出时间:</strong> {row['演出日期'].strftime('%Y年%m月%d日')} {row['演出时间']}</div>
                            <div class="theater-name">{row['剧院名称']}</div>
                            <div><strong>票价:</strong> {row['票价范围']}</div>
                            <p style="margin: 10px 0;">{row['简介']}</p>
                            <a href="{row['购票链接']}" target="_blank"><button>立即购票</button></a>
                        </div>
                        <div style="flex: 0 0 150px; margin-left: 15px;">
                            <img src="{row['海报图片']}" style="width: 100%; border-radius: 5px;">
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    # 表格视图
    if filtered_df.empty:
        st.warning("没有找到符合条件的演出")
    else:
        st.dataframe(
            filtered_df.drop(columns=["购票链接", "海报图片"]),
            column_config={
                "演出日期": st.column_config.DateColumn(
                    "演出日期",
                    format="YYYY年MM月DD日"
                )
            }
        )

with tab3:
    # 地图视图 (需要实际的地理坐标数据)
    st.header("演出地点分布")
    
    # 示例剧院坐标 (经度, 纬度)
    theater_coords = {
        "她剧场": [121.481453,31.242095],
        "十一楼哪个剧场": [121.484589,31.2399],
        "上海茉莉花剧场": [121.484995,31.236015],
        "北京保利剧院": [116.442332,39.940532],
        "大世界": [121.485864,31.234196],
        "墨剧场": [121.481453,31.242095]
    }
    
    # 添加坐标到数据
    map_df = filtered_df.copy()
    map_df["latitude"] = map_df["剧院名称"].map(lambda x: theater_coords.get(x, [None])[1])
    map_df["longitude"] = map_df["剧院名称"].map(lambda x: theater_coords.get(x, [None])[0])
    
    if not map_df.empty:
        fig = px.scatter_mapbox(
            map_df,
            lat="latitude",
            lon="longitude",
            hover_name="剧目名称",
            hover_data=["剧院名称", "演出日期", "票价范围"],
            color="剧院名称",
            zoom=4,
            height=600
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("没有数据可显示在地图上")

# 添加新演出表单
st.markdown("---")
st.header("添加新演出")

with st.form("add_performance"):
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("剧目名称*")
        theater = st.text_input("剧院名称*")
        date = st.date_input("演出日期*", min_value=datetime.now())
    
    with col2:
        time = st.time_input("演出时间*", datetime.strptime("19:30", "%H:%M"))
        price_range = st.text_input("票价范围* (例如: 280-1280元)")
        ticket_link = st.text_input("购票链接")
    
    description = st.text_area("剧目简介")
    poster_url = st.text_input("海报图片URL")
    
    submitted = st.form_submit_button("提交新演出")
    
    if submitted:
        if not all([title, theater, date, time, price_range]):
            st.error("请填写所有必填字段(标有*)")
        else:
            # 这里应该将数据保存到数据库或文件中
            st.success(f"已添加 '{title}' 的演出信息!")
            st.balloons()

# 关于部分
st.markdown("---")
st.markdown("""
**关于这个应用**
- 数据来源: 各大剧院官网
- 最后更新时间: {}
- 开发者: 張沁丹的狗
""".format(datetime.now().strftime("%Y年%m月%d日")))


# In[ ]:




