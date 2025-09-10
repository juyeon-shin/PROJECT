# 라이브러리 불러오기 
import pandas as pd
import streamlit as st
import numpy as np
import folium
from streamlit_folium import folium_static
#from streamlit_folium import folium_events
from datetime import date
import datetime
import matplotlib.pyplot as plt
import time
import folium
from folium.plugins import MarkerCluster
from datetime import date
plt.rcParams['font.family'] = 'Malgun Gothic'
import seaborn as sns
import plotly.express as px
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False





def main():
    ## 사이드바 
    st.sidebar.title('🤏 POPUP concept .ᐟ')
    brand = st.sidebar.text_input("**팝업 진행 브랜드를 입력하세요.**","") 
    st.sidebar.markdown(" ")
    st.subheader('🤏' + f' _:green[**{brand}**]_' + " 에 딱맞는 팝업 공간을 알아보세요.ᐟ", divider='green')
    
    # 분위기 선택
    atmosphere = st.sidebar.radio(
        "**희망 지역 분위기를 선택하세요.**",
        ('자연친화적 분위기', '문화적 분위기', '노스텔직 분위기', '전통적 분위기', '인더스트리얼 분위기')
    )
    st.caption("✅ " + atmosphere)
    st.sidebar.markdown(" ")
    
    # 업종 선택
    shop_options = ['가전/가구', '교육', '디저트', '럭셔리', '미용', '여행/숙박', '스포츠', '주류', '음식', '일상', '자동차', '패션']
    shop = st.sidebar.multiselect(
        "**진행하는 브랜드 업종을 선택하세요.**",
        shop_options,
        default=shop_options[:2]
    )
    st.sidebar.markdown(" ")
    st.caption("✅ " + ', '.join(shop))

    # 이벤트 진행 기간 선택
    start_date = st.sidebar.date_input("**운영 시작 날짜를 선택하세요.**", date.today())
    end_date = st.sidebar.date_input("**운영 종료 날짜를 선택하세요.**", start_date)

    # 날짜 포맷 변환
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # 날짜 검증 및 표시
    if start_date <= end_date:
        st.sidebar.success(f'선택한 운영 기간: {start_date_str}부터 {end_date_str}까지')
    else:
        st.sidebar.error('종료 날짜는 시작 날짜 이후여야 합니다.')

    st.caption(f"✅ {start_date_str} ~ {end_date_str}")
    
    st.markdown(" ")

    with st.spinner('분석이 진행 중이에요.'):
        time.sleep(5)
        
    ######################################################################################################
    ############### 전처리 ###############
    ## 데이터 선택
    data = pd.read_csv('Desktop/bigpro/total_data/최종데이터셋_위경도포함.csv')
    main_col = ['name', 'real_add', '자치구 행정동', '총층수', '1층포함여부', '총평수', '수용인원수',
                '평당가격', '공간크기','역번호','랜드마크','카페','버스정류장','도로 등 비율(%)','Latitude','Longitude']
    
    # 기간 선택
    def Select_period(start, end):
        start_month = pd.to_datetime(start).month
        end_month = pd.to_datetime(end).month
        month_list = list(range(start_month, end_month + 1))
        start_quarter = pd.to_datetime(start).quarter
        end_quarter = pd.to_datetime(end).quarter
        quarter_list = list(range(start_quarter, end_quarter + 1))
        return month_list, quarter_list
    
    def Select_month(month_list):
        month_col = []
        for month in month_list:
            month_col.append(f'2030 생활인구 {month}월')
            month_col.append(f'2023년{month}월행사')
        return month_col


    # 컨셉 선택
    def Select_concept(concept_input):
        concept_col = []
        concept_dict = {'자연친화적 분위기': ['자연 비율(%)'],'인더스트리얼 분위기': ['공장용지 등 비율(%)'],'전통적 분위기': ['한옥 개수'],
                        '문화적 분위기': ['예술_컨셉','갤러리_컨셉','음악_컨셉'], '노스텔직 분위기' : ['골목_컨셉']}
    
        for key in concept_input:
            concept_col += concept_dict[key]
        return concept_col
    
    def Select_category(category_input):
        category_col = []
        for quater in quater_list:
            category_dict = {'음식' : [f'기타요식 금액비율_{quater}분기',f'음/식료품 금액비율_{quater}분기', f'일식/중식/양식 금액비율_{quater}분기',
                                     f'한식 금액비율_{quater}분기', f'기타요식 건수비율_{quater}분기',f'음/식료품 건수비율_{quater}분기', 
                                     f'일식/중식/양식 건수비율_{quater}분기',f'한식 건수비율_{quater}분기'], 
                             '디저트' : [f'제과/커피/패스트푸드 금액비율_{quater}분기', f'제과/커피/패스트푸드 건수비율_{quater}분기'],
                             '가전/가구' : [f'가전/가구 금액비율_{quater}분기',f'인테리어 금액비율_{quater}분기', 
                                        f'가전/가구 건수비율_{quater}분기',f'인테리어 건수비율_{quater}분기'],
                             '교육' :  [f'교육용품 금액비율_{quater}분기',f'학원 금액비율_{quater}분기', f'유아교육 금액비율_{quater}분기',
                                      f'교육용품 건수비율_{quater}분기',f'학원 건수비율_{quater}분기', f'유아교육 건수비율_{quater}분기'], 
                             '자동차' : [f'자동차서비스/용품 금액비율_{quater}분기', f'자동차판매 금액비율_{quater}분기',f'주유 금액비율_{quater}분기',
                                      f'자동차서비스/용품 건수비율_{quater}분기', f'자동차판매 건수비율_{quater}분기',f'주유 건수비율_{quater}분기'],
                             '여행/숙박' : [f'숙박 금액비율_{quater}분기',f'여행 금액비율_{quater}분기',
                                       f'숙박 건수비율_{quater}분기',f'여행 건수비율_{quater}분기'], 
                             '스포츠' : [f'스포츠/문화/레저 금액비율_{quater}분기', f'스포츠/문화/레저용품 금액비율_{quater}분기',
                                      f'스포츠/문화/레저 건수비율_{quater}분기', f'스포츠/문화/레저용품 건수비율_{quater}분기'], 
                             '미용' : [f'미용서비스 금액비율_{quater}분기', f'화장품 금액비율_{quater}분기',
                                     f'미용서비스 건수비율_{quater}분기', f'화장품 건수비율_{quater}분기'], 
                             '패션' : [f'의복/의류 금액비율_{quater}분기', f'패션/잡화 금액비율_{quater}분기',
                                     f'의복/의류 건수비율_{quater}분기', f'패션/잡화 건수비율_{quater}분기'], 
                             '일상' : [f'편의점 금액비율_{quater}분기', f'할인점/슈퍼마켓 금액비율_{quater}분기',
                                     f'편의점 건수비율_{quater}분기', f'할인점/슈퍼마켓 건수비율_{quater}분기'],
                             '주류' : [f'유흥 금액비율_{quater}분기', f'유흥 건수비율_{quater}분기'], 
                             '럭셔리' : [f'백화점 금액비율_{quater}분기', f'백화점 건수비율_{quater}분기']}
            for key in category_input:
                category_col += category_dict[key]
        return category_col
    
    ## 사이드바에서 입력받음 (기간,컨셉,업종)
    start, end = start_date_str, end_date_str
    concept_input = [atmosphere]
    category_input = list(shop)

    month_list, quater_list = Select_period(start, end)
    month_col = Select_month(month_list)
    concept_col = Select_concept(concept_input)
    category_col = Select_category(category_input)
    
    ## 최종 칼럼 선택 
    chosen_col = main_col + month_col + concept_col + category_col
    chosen_data = data[chosen_col]
    
    
    ## 전처리
    def model_processing(chosen_data):
        obj_col = list(chosen_data.select_dtypes('object').columns)
        num_data = chosen_data.drop(obj_col,axis=1) # 스케일링을 위해 범주형 제외
    
        ## 스케일링 : 칼럼이 선택되는 것에 따라 스케일링이 따로 진행됨
        from sklearn.preprocessing import MinMaxScaler
        Scaler = MinMaxScaler()
        Scaled = Scaler.fit_transform(num_data)
        return Scaled
    Scaled = model_processing(chosen_data)
    
    from sklearn.cluster import KMeans

    k_means = KMeans(n_clusters = 3, init='k-means++', random_state=2024)
    k_means.fit_predict(Scaled)
    chosen_data['cluster'] = k_means.labels_
    
    cluster_0_all = chosen_data[chosen_data['cluster'] == 0]
    cluster_1_all = chosen_data[chosen_data['cluster'] == 1]
    cluster_2_all = chosen_data[chosen_data['cluster'] == 2]
    
    cluster_0 = chosen_data[chosen_data['cluster'] == 0][['name','1층포함여부','총평수','평당가격','공간크기','real_add','Latitude','Longitude']]
    cluster_1 = chosen_data[chosen_data['cluster'] == 1][['name','1층포함여부','총평수','평당가격','공간크기','real_add','Latitude','Longitude']]
    cluster_2 = chosen_data[chosen_data['cluster'] == 2][['name','1층포함여부','총평수','평당가격','공간크기','real_add','Latitude','Longitude']]
    
    ######################################################################################################
    ################## 대시보드 시작 ##################
    
    tab1, tab2, tab3 = st.tabs([" A그룹 ", " B그룹 ", " C그룹 "])
    with tab1:
        st.subheader(":red[A그룹]의 경쟁력은,")
        st.markdown(" ")
        
        cluster_0.rename(columns={'name': '건물명', 'real_add': '상세주소','Latitude':'LAT','Longitude':'LON'}, inplace=True)
        cluster_0 = cluster_0.reset_index(drop=True)
        cluster_a = cluster_0[['건물명','1층포함여부','총평수','평당가격','공간크기','상세주소']]
        
        ############################## 대시보드 함수 ##############################
        
        # 데이터프레임
        def data_show(cluster):
            
            st.markdown("📍 **[🤗간단] 팝업 공간 정보**")
            st.dataframe(cluster)
            st.markdown(" ")
            
        def data_all_show(cluster):
            st.markdown("📍 **[🤔상세] 팝업 공간 상세 정보**")
            cluster_ = cluster.reset_index(drop=True)
            st.dataframe(cluster_)
            st.markdown(" ")
            
        # 지도 마커
        color_list = ['purple', 'orange', 'lightblue']
        def map_show(cluster, color):
            df = cluster[['건물명','LAT','LON']]
            m = folium.Map(location=[max(df['LAT']), max(df['LON'])], zoom_start=12)
            for idx, row in df.iterrows():
                folium.Marker(
                    location=[row['LAT'], row['LON']],
                    popup=row['건물명'],
                    icon=folium.Icon(icon="info-sign", color=color)).add_to(m)
            st.markdown(" ")
            st.markdown("🌏 **팝업 공간 위치**")
            folium_static(m, width=700, height=350)
            st.markdown(" ")
            
        # 평균 비교
        def mean_def(cluster):
            col1, col2, col3 = st.columns(3)
            with col1:
                mean = round(np.mean(cluster['총평수']),2)
                chosen_data_mean = round(np.mean(chosen_data['총평수']),2)
                diff = round(mean - chosen_data_mean,2)
                st.metric(label='공간 크기', value=f'{mean}㎡', delta=f'{diff}㎡')
                
                mean = round(np.mean(cluster['카페']),2)
                chosen_data_mean = round(np.mean(chosen_data['카페']),2)
                diff = round(mean - chosen_data_mean,2)
                st.metric(label='카페 개수', value=f'{mean}개', delta=f'{diff}')
                
            with col2:
                mean = round(np.mean(cluster['평당가격']), 2)
                chosen_data_mean = round(np.mean(chosen_data['평당가격']), 2)
                diff = round(mean - chosen_data_mean, 2)
                formatted_mean = f"{mean*24:,.0f}원"
                formatted_diff = f"{diff*24:,.0f}원"
                st.metric(label='1㎡ 당 하루 가격', value=formatted_mean, delta=formatted_diff)

                
                mean = round(np.mean(cluster['랜드마크']),2)
                chosen_data_mean = round(np.mean(chosen_data['랜드마크']),2)
                diff = round(mean - chosen_data_mean,2)
                st.metric(label='랜드마크 개수', value=f'{mean}개', delta=f'{diff}개')
            
            with col3:
                mean = round(np.mean(cluster['역번호']),2)
                chosen_data_mean = round(np.mean(chosen_data['역번호']),2)
                diff = round(mean - chosen_data_mean,2)
                st.metric(label='지하철역 개수', value=f'{mean}개', delta=f'{diff}개')
                
                mean = round(np.mean(cluster['버스정류장']),2)
                chosen_data_mean = round(np.mean(chosen_data['버스정류장']),2)
                diff = round(mean - chosen_data_mean,2)
                st.metric(label='버스정류장 개수', value=f'{mean}개', delta=f'{diff}개')
                
        
        # 생활인구 그래프
        def man_graph(cluster, key):
            month_man = []
            for month in month_list:    
                month_man.append(f'2030 생활인구 {month}월')
            month_man_select = st.selectbox('원하는 월을 선택하세요.', month_man,  key=f'{key}man')
            st.caption(f'🙋🏻참고1) :red[빨간색 선]은 {month_man_select}의 전지역 평균이에요.')
            st.caption(f'🙋🏻참고2) :red[생활인구]는 공간이 속한 행정동에 체류하고 있는 사람이에요.')
            selected_month_data = cluster[['name', month_man_select]]
            mean_value = np.mean(chosen_data[f'{month_man_select}'])
            plt.figure(figsize=(10, 6))
            colors = sns.color_palette('summer', len(selected_month_data['name']))
            plt.bar(selected_month_data['name'], selected_month_data[month_man_select],color=colors)
            plt.plot(selected_month_data['name'], selected_month_data[month_man_select], color='green', linestyle='--', marker='o', linewidth=1,markersize=3) 
            plt.axhline(y=mean_value, color='#e35f62', linewidth=2)
            plt.ylabel('생활인구')
            plt.title(f'{month_man_select} 공간별 평균 생활인구')
            plt.xticks(rotation=-90, fontsize=5)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.grid(False)
            st.pyplot(plt)
            
            st.markdown(" ")
            
        # 행사 그래프
        def event_graph(cluster, key):
            month_event = []
            for month in month_list:
                month_event.append(f'2023년{month}월행사')
            month_event_select = st.selectbox('원하는 월을 선택하세요.', month_event,  key=f'{key}event')
            selected_month_data = cluster[['name', month_event_select]]

            plt.figure(figsize=(10, 6))
            plt.ylim(0, max(selected_month_data[month_event_select]) * 1.1)
            plt.plot(selected_month_data['name'], selected_month_data[month_event_select], color='#e35f62', linestyle='--', marker='o',linewidth=1,markersize=3)
            plt.ylabel('행사 수')
            plt.title(f'{month_event_select} 근처 행사 수')
            plt.xticks(rotation=-90, fontsize=5)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.grid(False)
            st.pyplot(plt)
            
            st.markdown(" ")
        
        # 분위기 그래프
        def mood(cluster):
            concept_col = Select_concept(concept_input)
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
            fig, ax = plt.subplots(figsize=(10, 6))
            for idx, col in enumerate(concept_col):
                ax.plot(cluster['name'], cluster[col], marker='o', label=col,markersize=3, color=colors[idx % len(colors)])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.set_ylabel('분위기 관련 수치')
            ax.set_title(f'{concept_input[0]}에 따른 장소별 분위기')
            ax.tick_params(axis='x', rotation=-90, labelsize=5)
            ax.grid(False)
            ax.legend()
            st.pyplot(fig)

            
        # 카드 그래프
        def sales_graph(cluster, quarter_list, category_input,key):
            selected_quarter = st.selectbox('원하는 분기(quarter)를 선택하세요.', quarter_list, key=f'{key}quq')
            # selected_category = st.selectbox('업종을 선택하세요', category_input, key=f'{key}caq')
            filtered_amount_columns = [col for col in category_col if '금액비율' in col and f'_{selected_quarter}분기' in col]
            filtered_count_columns = [col for col in category_col if '건수비율' in col and f'_{selected_quarter}분기' in col]

            # 금액비율 막대 그래프
            plt.figure(figsize=(10, 6))
            for col in filtered_amount_columns:
                value = cluster[col].max()
                plt.bar(col, value)
                plt.text(col, value, f'{value*100:.2f}%', ha='center', va='bottom')
            x_labels = [col.split(' 금액비율')[0] for col in filtered_amount_columns]
            plt.xticks(range(len(filtered_amount_columns)), x_labels, rotation=0, fontsize=10)
            plt.ylabel('카드 결제 금액 비율')
            plt.title(f'{selected_quarter}분기의 최대 카드 결제 금액 비율')
            plt.xticks(rotation=0, fontsize=10)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            st.pyplot(plt)
            
            st.markdown(" ")
            
            # 건수비율 막대 그래프
            plt.figure(figsize=(10, 6))
            for col in filtered_count_columns:
                value = cluster[col].max()
                plt.bar(col, value)
                plt.text(col, value, f'{value*100:.2f}%', ha='center', va='bottom')
            x_labels = [col.split(' 금액비율')[0] for col in filtered_amount_columns]
            plt.xticks(range(len(filtered_amount_columns)), x_labels, rotation=0, fontsize=10)
            plt.ylabel('카드 결제 금액 비율')
            plt.title(f'{selected_quarter}분기의 최대 카드 결제 건수 비율')
            plt.xticks(rotation=0, fontsize=10)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            st.pyplot(plt)
            
        ##########################################################################
        # tab1
        data_show(cluster_a)
        if st.checkbox("체크를 누르면, 상세 정보를 확인할 수 있어요!", key='checkbox1'):
            data_all_show(cluster_0_all)
            st.markdown(" ")
        
        map_show(cluster_0, color_list[0])
        
        st.markdown('💡 **A군집의 평균은 이렇군요!**')
        mean_def(cluster_0_all)
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('📊 **A군집 공간의 월별 생활인구를 확인해보세요!**')
        man_graph(cluster_0_all,1)
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('🤹‍♀️ **A군집 공간의 월별 행사 수를 확인해보세요!**')
        event_graph(cluster_0_all,1)

        st.markdown(" ")
        st.markdown(" ")
        st.markdown('🤹‍♀️ **A군집 공간의 분위기를 확인해보세요!**')
        mood(cluster_0_all)
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('💸 **A군집 공간의 업종별 카드 소비를 확인해보세요!**')
        month_list, quarter_list = Select_period(start_date, end_date)
        category_dict = Select_category(category_input)
        sales_graph(cluster_0_all, quarter_list, category_input,1)

        
    with tab2:
        st.subheader(":red[B그룹]의 경쟁력은,")
        cluster_1.rename(columns={'name': '건물명', 'real_add': '상세주소','Latitude':'LAT','Longitude':'LON'}, inplace=True)
        cluster_1 = cluster_1.reset_index(drop=True)
        cluster_b = cluster_1[['건물명','1층포함여부','총평수','평당가격','공간크기','상세주소']]
        
        data_show(cluster_b)
        if st.checkbox("체크를 누르면, 상세 정보를 확인할 수 있어요!", key='checkbox2'):
            data_all_show(cluster_1_all)

        map_show(cluster_1, color_list[1])
        st.markdown('💡 **B군집의 평균은 이렇군요!**')
        mean_def(cluster_1_all)
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('📊 **B군집 공간의 월별 생활인구를 확인해보세요!**')
        man_graph(cluster_1_all,2)
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('🤹‍♀️ **B군집 공간의 월별 행사 수를 확인해보세요!**')
        event_graph(cluster_1_all,2)
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('🤹‍♀️ **B군집 공간의 분위기를 확인해보세요!**')
        mood(cluster_1_all)
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('💸 **B군집 공간의 업종별 카드 비율을 확인해보세요!**')
        month_list, quarter_list = Select_period(start_date, end_date)
        category_dict = Select_category(category_input)
        sales_graph(cluster_1_all, quarter_list, category_input,2)
        
    with tab3:
        st.subheader(":red[C그룹]의 경쟁력은,")
        cluster_2.rename(columns={'name': '건물명', 'real_add': '상세주소','Latitude':'LAT','Longitude':'LON'}, inplace=True)
        cluster_2 = cluster_2.reset_index(drop=True)
        cluster_c = cluster_2[['건물명','1층포함여부','총평수','평당가격','공간크기','상세주소']]
        
        data_show(cluster_c)
        if st.checkbox("체크를 누르면, 상세 정보를 확인할 수 있어요!", key='checkbox3'):
            data_all_show(cluster_2_all)

        map_show(cluster_2, color_list[2])
        
        st.markdown('💡 **C군집의 평균은 이렇군요!**')
        mean_def(cluster_2_all)
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('📊 **C군집 공간의 월별 생활인구를 확인해보세요!**')
        man_graph(cluster_2_all,3)
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('🤹‍♀️ **C군집 공간의 월별 행사 수를 확인해보세요!**')
        event_graph(cluster_2_all,3)           
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('🤹‍♀️ **C군집 공간의 분위기를 확인해보세요!**')
        mood(cluster_2_all)
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('💸 **C군집 공간의 업종별 카드 비율을 확인해보세요!**')
        month_list, quarter_list = Select_period(start_date, end_date)
        category_dict = Select_category(category_input)
        sales_graph(cluster_1_all, quarter_list, category_input,3)
    

# 실행
if __name__ == "__main__":
    main()

##### 로딩화면 구현 #####
# import time 

# # 방법 1 progress bar 
# latest_iteration = st.empty()
# bar = st.progress(0)

# for i in range(100):
#   # Update the progress bar with each iteration.
#   latest_iteration.text(f'Iteration {i+1}')
#   bar.progress(i + 1)
#   time.sleep(0.05)
#   # 0.05 초 마다 1씩증가