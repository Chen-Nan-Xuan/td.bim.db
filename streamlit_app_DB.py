import streamlit as st
import pandas as pd
import altair as alt
import pandas as pd
import numpy as np
# import time

# 設定頁面配置
st.set_page_config(page_title="建築材料資料庫")

# 設定 CSS
st.markdown("""
    <style>
    body {
        font-family: 'Microsoft JhengHei', sans-serif;
        background-color: #f4f4f4;
    }
    h1 {
        color: #276ac2;  
        font-size: 2.5em;
        text-align: center;
        margin-top: 30px;
    }
    h2 {
        color: #333;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
    }
    .stButton > button {
        background-color: #276ac2;  
        color: white;
        border-radius: 5px;
        padding: 10px;
        margin-top: 20px;
    }
    .stImage {
        display: block;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

# 載入資料
data = pd.read_csv('data.csv')

# 主頁
def main_page():
    st.title("🗂️ 建築材料資料庫")
    st.markdown('***')
    st.markdown("##### 歡迎使用建築材料資料庫！請選擇左側目錄中的功能。")
    st.markdown('***')
    st.markdown('#### 【使用說明】')
    st.info('建築材料資料庫，可以簡稱為「建材資料庫」或「資料庫」，主要為了整合BIM中心年度目標的共同資訊，以及整合各組工作所需的內容，使取得資訊變得更加便利。')
    st.markdown('#### 【定義說明】') 
    st.info('建築材料資料庫（簡稱為「建材資料庫」或「資料庫」）的資訊涵蓋廣泛，有材料的規格、樣式、尺寸、施工流程及方法，以及Revit族群的設定、檔案等資訊，因此針對資料庫產出【原則訂定】，以利後續作業。')
    # 版本和日期
    st.markdown("#### 【版本資訊】")
    st.info("版本: 1.0.0\n發佈日期: 2024-11-01")
    # 公司版權與製作者
    st.markdown('***')
    st.write('營造股份有限公司 2024 © Designed by Nan-Xuan.')

# 子頁：建材資料查詢頁
def query_page():
    st.title("🔬 建材資料查詢") 
    st.markdown('***')
    st.markdown("##### 請選擇左側目錄中的項目進行查詢。")

    # 初始化 session_state
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = '土建類'
        st.session_state.selected_spot = '未指定'
        st.session_state.selected_brand = '未指定'
        st.session_state.selected_material_type = '未指定'
        st.session_state.selected_material_property = '未指定'
        st.session_state.selected_composition = '未指定'

    # 選擇建材類型
    selected_page = st.sidebar.selectbox('選擇欲查詢的建材類型', ['土建類', '機電類'], index=['土建類', '機電類'].index(st.session_state.selected_page))
    st.session_state.selected_page = selected_page

    # 選擇工程階段
    spots = {
        '土建類': ['未指定', '擋土工程', '結構工程', '結構補強工程', '天花板工程', '地坪工程', 
                  '外牆工程', '帷幕工程', '電梯工程', '裝修工程', '整修工程', '門窗工程', 
                  '油漆工程', '屋頂工程', '防水工程', '浴廁工程', '給排水工程', 
                  '電力工程', '弱電設備工程', '消防工程', '空調工程'],
        '機電類': ['未指定', '給水工程', '排水工程', '排汙工程', '弱電工程', '電氣工程', '消防工程']
    }
    selected_spot = st.sidebar.selectbox('選擇工程階段', spots[selected_page], index=spots[selected_page].index(st.session_state.selected_spot))
    st.session_state.selected_spot = selected_spot

    # 動態過濾廠牌名稱
    filtered_brands = data[data['類型'] == selected_page]['廠牌名稱'].unique()
    brands = ['未指定'] + filtered_brands.tolist()
    selected_brand = st.sidebar.selectbox('選擇廠牌名稱', brands, index=brands.index(st.session_state.selected_brand))
    st.session_state.selected_brand = selected_brand

    # 動態過濾材料類別
    filtered_material_types = data[
        (data['類型'] == selected_page) & 
        (data['工程階段'] == selected_spot)]['材料類別'].unique()
    material_types = ['未指定'] + filtered_material_types.tolist()
    selected_material_type = st.sidebar.selectbox('選擇材料類別', material_types, index=material_types.index(st.session_state.selected_material_type))
    st.session_state.selected_material_type = selected_material_type

    # 動態過濾材料性質
    filtered_material_properties = data[
        (data['類型'] == selected_page) & 
        (data['工程階段'] == selected_spot) &
        (data['材料類別'] == selected_material_type)]['材料性質'].unique()
    material_properties = ['未指定'] + filtered_material_properties.tolist()
    selected_material_property = st.sidebar.selectbox('選擇材料性質', material_properties, index=material_properties.index(st.session_state.selected_material_property))
    st.session_state.selected_material_property = selected_material_property

    # 動態過濾組成材質
    filtered_compositions = data[
        (data['類型'] == selected_page) & 
        (data['工程階段'] == selected_spot) &
        (data['材料類別'] == selected_material_type) &
        (data['材料性質'] == selected_material_property)]['組成材質'].unique()
    compositions = ['未指定'] + filtered_compositions.tolist()
    selected_composition = st.sidebar.selectbox('選擇組成材質', compositions, index=compositions.index(st.session_state.selected_composition))
    st.session_state.selected_composition = selected_composition

    # 搜尋輸入框
    search_query = st.sidebar.text_input("關鍵字搜尋", placeholder="輸入關鍵字後請按查詢...")

    # 清空選擇按鈕
    if st.sidebar.button('清空選擇'):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()

    # 查詢按鈕
    if st.sidebar.button('查詢'):
        # 構建過濾條件
        filters = (data['類型'] == selected_page)

        if selected_spot != '未指定':
            filters &= (data['工程階段'] == selected_spot)

        if selected_brand != '未指定':
            filters &= (data['廠牌名稱'] == selected_brand)

        if selected_material_type != '未指定':
            filters &= (data['材料類別'] == selected_material_type)

        if selected_material_property != '未指定':
            filters &= (data['材料性質'] == selected_material_property)

        if selected_composition != '未指定':
            filters &= (data['組成材質'] == selected_composition)

        # 根據過濾條件過濾資料
        filtered_data = data[filters]

        # 搜尋資料
        if search_query:
            filtered_data = filtered_data[
                filtered_data['材料類別'].str.contains(search_query, case=False, na=False) |
                filtered_data['材料名稱'].str.contains(search_query, case=False, na=False) |
                filtered_data['廠牌名稱'].str.contains(search_query, case=False, na=False)
            ]

        if not filtered_data.empty:
            st.write('查詢資訊如下：')
            filtered_data = filtered_data.drop(columns=['最後編輯者', '官網連結', '材料價格', '組成材質', '適用空間', '空間內外', '最後編輯時間'], errors='ignore')
            st.dataframe(filtered_data, use_container_width=True)
        else:
            st.write('沒有找到相關資料。')

# 子頁：建模資料查詢頁
def modeling_data_query_page():
    st.title("🏛️ 建模資料查詢")
    st.markdown('***')
    st.markdown("##### 請選擇左側目錄中的項目進行查詢。")

    # 選擇建材類型
    selected_modeling_data = st.sidebar.selectbox('材料類別', data['材料類別'].unique().tolist())

    # 查詢按鈕
    if st.sidebar.button('查詢建模資料'):
        modeling_data_info = data[data['材料類別'] == selected_modeling_data]
        
        if not modeling_data_info.empty:
            st.write(f'查詢的建模資料類別為： {selected_modeling_data}')
            st.write('建模資料資訊如下：')
            st.dataframe(modeling_data_info[['廠牌名稱', '材料類別', '材料名稱', '建模尺寸']], use_container_width=True)

            # 假設圖片路徑在資料中有一欄叫做 '圖片路徑'
            if '圖片路徑' in modeling_data_info.columns:
                image_path = modeling_data_info.iloc[0]['圖片路徑']  # 取第一筆資料的圖片路徑
                file_name = 'BM_001.png'  # 指定檔名
                
                # 顯示圖片
                st.image(image_path, caption='查詢的建模資料圖片', use_column_width=True)

                # 添加下載按鈕
                with open('BM_001', "rb") as f:
                    st.download_button(
                        label="下載建模資料圖片",
                        data=f,
                        file_name=file_name,
                        mime="image/png"
                    )
            else:
                st.write('目前沒有該材料的建模資訊圖片可供下載。')
        else:
            st.write('沒有找到該建模資料的資訊。')

# 子頁：建材價格查詢頁
def price_query_page():
    st.title("💰 建材價格查詢")
    st.markdown('***')
    st.markdown("##### 請選擇左側目錄中的項目進行查詢。")

    # 選擇建材類型
    selected_material = st.sidebar.selectbox('材料類別', data['材料類別'].unique().tolist())

    # 查詢按鈕
    if st.sidebar.button('查詢價格'):
        price_info = data[data['材料類別'] == selected_material]
        
        if not price_info.empty:
            st.write(f'查詢的建材名稱為： {selected_material}')
            st.write('價格資訊如下：')
            st.dataframe(price_info[['廠牌名稱', '材料名稱', '材料價格']], use_container_width=True)
        else:
            st.write('沒有找到該建材的價格資訊。')

# 子頁：資料數量統計頁
def stats_page():
    st.title("📈 資料數量統計")
    st.markdown('***')
    st.write("以下是資料數量統計資訊：")
    
    # 計算每種材料類別的數量
    material_count = data['材料類別'].value_counts().reset_index()
    material_count.columns = ['材料類別', '數量']

    # 使用 Altair 繪製折線圖
    line_chart = alt.Chart(material_count).mark_line(point=True).encode(
        x=alt.X('材料類別:O', title='材料類別', axis=alt.Axis(labelAngle=0)),  
        y=alt.Y('數量:Q', title='數量', axis=alt.Axis(labelAngle=0)),  
        tooltip=['材料類別', '數量']
    ).properties(
        title='材料類別數量統計',
        width=700,
        height=400
    ).configure_mark(
        color='steelblue'
    )

    # 在 Streamlit 中顯示圖表
    st.altair_chart(line_chart, use_container_width=True)
    st.markdown('***')
    st.write('營造股份有限公司 2024 © Designed by Nan-Xuan.')

# 主程式與多頁面應用
st.sidebar.title("建築材料資料庫目錄")
page = st.sidebar.selectbox("選擇頁面", ["主頁", "建材資料查詢", "建模資料查詢", "建材價格查詢", "資料數量統計"])

if page == "主頁":
    main_page()
elif page == "建材資料查詢":
    query_page()
elif page == "建模資料查詢":
    modeling_data_query_page()  # 修正為正確的函數調用
elif page == "建材價格查詢":
    price_query_page()
elif page == "資料數量統計":
    stats_page()
