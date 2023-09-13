# import os
# import fiona
import geopandas as gpd
import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import folium
from streamlit_folium import st_folium
from branca.colormap import linear
import csv


st.set_page_config(layout="wide")

st.sidebar.info(
    # """
    # - Web App URL: <https://streamlit.geemap.org>
    # - GitHub repository: <https://github.com/giswqs/streamlit-geospatial>
    # """
    """
    - ARCHITECTS 49: 
    <https://a49.co.th>
    """
)
# - Integrated Research and Innovations: <https://github.com/giswqs/streamlit-geospatial>

# st.sidebar.title("Contact")
# st.sidebar.info(
#     """
#     Qiusheng Wu: <https://wetlands.io>
#     [GitHub](https://github.com/giswqs) | [Twitter](https://twitter.com/giswqs) | [YouTube](https://www.youtube.com/c/QiushengWu) | [LinkedIn](https://www.linkedin.com/in/qiushengwu)
#     """
# )

# data = pd.read_csv('..//police.csv')
# data = pd.read_csv('.//data//data_showcase//police_station.csv')
# data.rename(columns={data.columns[0]: "name"},inplace = True)

# =========== RESIDENTIAL ===========
res = pd.read_csv("..//data//data_showcase//Residential Project Data_opendata_project.csv",sep=',')
res = res[res['province_name_en'] == 'Bangkok']
# data = pd.read_csv("police.csv",sep=',')
res = res[['name_th','longitude','latitude']]
res.columns = ['name', 'lng', 'lat']
res = res.dropna()
res = res.sample(500)

# =========== HEALTHCARE ===========
health = pd.read_csv('..//data//data_showcase//hospital.csv')
health.rename(columns={health.columns[0]: "name"},inplace = True)

# =========== MARKET ===========
market = pd.read_csv('..//data//data_showcase//market.csv')
market.rename(columns={market.columns[0]: "name"},inplace = True)

# =========== DEPARTMENT STORE ===========
dep_sto = pd.read_csv('..//data//data_showcase//department.csv')
dep_sto.rename(columns={dep_sto.columns[0]: "name"},inplace = True)

# =========== RESIDENTIAL ===========
fire = pd.read_csv('..//data//data_showcase//fire_station.csv')
fire.rename(columns={fire.columns[0]: "name"},inplace = True)

# =========== METRO STATION ===========
metro = pd.read_csv('..//data//data_showcase//mrt.csv')
metro.rename(columns={metro.columns[0]: "name"},inplace = True)

# =========== POLICESTATION ===========
police = pd.read_csv('..//data//data_showcase//police_station.csv')
police.rename(columns={police.columns[0]: "name"},inplace = True)

# =========== RESIDENTIAL ===========

# =========== RESIDENTIAL ===========




districts = gpd.read_file('..//data//data_showcase//district.json', encoding='utf-8')
districts['population'] = districts['num_male'] + districts['num_female']
min_population = districts['population'].min()
max_population = districts['population'].max()
# Define a colormap
colormap = linear.Blues_09.scale(min_population, max_population)

def style_function(feature):
    population = feature['properties']['population']
    return {
        'fillColor': colormap(population),
        'color': '#00f2ff',
        'weight': 1,
        'fillOpacity': 0.8
    }

def style_function0(feature):
    population = feature['properties']['population']
    return {
        # 'fillColor': colormap(population),
        'color': '#00f2ff',
        'weight': 0.1,
        'fillOpacity': 0
    }

def app():
    st.title("Restorative Bangkok City")
    map_border = folium.Map(location=[13.72930616838845, 100.57522025302703], tiles="Cartodbdark_matter", zoom_start=11)
    m2 = folium.Map(location=[13.72930616838845, 100.57522025302703], tiles="Cartodbdark_matter", zoom_start=11) # "Stamen Toner"
    row1_col0, row1_col1, row1_col2 = st.columns([3, 3, 1])
    width = 950
    height = 600

    with row1_col0:
        # with st.expander("See source code"):
                # with st.echo():
                folium.GeoJson(
                    districts,
                    style_function=style_function0,
                    highlight_function=lambda x: {'weight': 3, 'color': '#3f999e', 'fillOpacity': 0.7 },
                    tooltip=folium.GeoJsonTooltip(fields=['dname', 'population'], labels=False, sticky=True)
                ).add_to(map_border)

                # =========== RESIDENTIAL ===========
                for lat, lng, name in zip(res['lat'].astype(float), res['lng'].astype(float), res['name'] ):
                    folium.CircleMarker(
                        [lat, lng],
                        radius=3,
                        color= None, #'#fa7202',
                        fill=True,
                        popup=folium.Popup(name, max_width="100"),
                        fill_color='#fa7202',
                        fill_opacity=0.3,
                        parse_html=False
                    ).add_to(map_border)

                # =========== HEALTHCARE ===========
                for lat, lng, name in zip(health['lat'].astype(float), health['lng'].astype(float), health['name']):
                    folium.Circle([lat, lng],
                                radius=2500, # 5000 meters
                                color= None, #'#f100f5',
                                fill=True,
                                popup=folium.Popup(name, max_width="100"),
                                fill_color='#f100f5',
                                fill_opacity=0.5
                                ).add_to(map_border)
                st_folium(map_border, width=-1400, height= 800, returned_objects=[])


    with row1_col2:
        

        backend = st.selectbox(
            "Select a livability type", ["Population", "Environmental score", "Happiness score"], index=0
        )
        
        # backend2 = st.selectbox(
        #     "Select dataset", ["Metro Train Station", "Park", "Healthcare", "Market","Department Store", "Fire Station", "Police Station" , "Community"], index=0
        # )
        backend2 = st.multiselect(
            'Select dataset',
            ["Metro Train Station", "Healthcare", "Market","Department Store", "Fire Station", "Police Station" , "Community"],
            ['Metro Train Station'])

        st.markdown(
             "**" + backend+ "**"  +  " and"  + " " + "**" + backend2[0]+ "**" 
            )
        check = st.checkbox("Select by District", value = False, key="disabled")
        
        if check:
            option = st.selectbox(  
                "How would you like to be contacted?",
                (
                    "Phra Nakhon (พระนคร)",
                    "Dusit (ดุสิต)",
                    "Nong Chok (หนองจอก)",
                    "Bang Rak (บางรัก)",
                    "Bang Khen (บางเขน)",
                    "Bang Kapi (บางกะปิ)",
                    "Pathum Wan (ปทุมวัน)",
                    "Pom Prap Sattru Phai (ป้อมปราบศัตรูพ่าย)",
                    "Phra Khanong (พระโขนง)",
                    "Min Buri (มีนบุรี)",
                    "Lat Krabang (ลาดกระบัง)",
                    "Yan Nawa (ยานนาวา)",
                    "Samphanthawong (สัมพันธวงศ์)",
                    "Phaya Thai (พญาไท)",
                    "Thon Buri (ธนบุรี)",
                    "Bangkok Yai (บางกอกใหญ่)",
                    "Huai Khwang (ห้วยขวาง)",
                    "Khlong San (คลองสาน)",
                    "Taling Chan (ตลิ่งชัน)",
                    "Bangkok Noi (บางกอกน้อย)",
                    "Bang Khun Thian (บางขุนเทียน)",
                    "Phasi Charoen (ภาษีเจริญ)",
                    "Nong Khaem (หนองแขม)",
                    "Rat Burana (ราษฎร์บูรณะ)",
                    "Bang Phlat (บางพลัด)",
                    "Din Daeng (ดินแดง)",
                    "Bueng Kum (บึงกุ่ม)",
                    "Sathon (สาทร)",
                    "Bang Sue (บางซื่อ)",
                    "Chatuchak (จตุจักร)",
                    "Bang Kho Laem (บางคอแหลม)",
                    "Prawet (ประเวศ)",
                    "Khlong Toei (คลองเตย)",
                    "Suan Luang (สวนหลวง)",
                    "Chom Thong (จอมทอง)",
                    "Don Mueang (ดอนเมือง)",
                    "Ratchathewi (ราชเทวี)",
                    "Lat Phrao (ลาดพร้าว)",
                    "Watthana (วัฒนา)",
                    "Bang Khae (บางแค)",
                    "Lak Si (หลักสี่)",
                    "Sai Mai (สายไหม)",
                    "Khan Na Yao (คันนายาว)",
                    "Saphan Sung (สะพานสูง)",
                    "Wang Thonglang (วังทองหลาง)",
                    "Khlong Sam Wa (คลองสามวา)",
                    "Bang Na (บางนา)",
                    "Thawi Watthana (ทวีวัฒนา)",
                    "Thung Khru (ทุ่งครุ)",
                    "Bang Bon (บางบอน)"
                    ),
                label_visibility='collapsed',
                # abled = st.session_state.disabled
                # disabled=st.session_state.disabled,
            )
        # print(option)
        # พระนคร
        if check and option:
            if option == 'Phra Nakhon (พระนคร)':
                map_border = folium.Map(location=[13.7573, 100.4951], tiles="Cartodbdark_matter", zoom_start=14)
            elif option == 'Khlong Toei (คลองเตย)':
                map_border = folium.Map(location=[13.7189, 100.5672], tiles="Cartodbdark_matter", zoom_start=14)
            else:
                map_border = folium.Map(location=[13.7573, 100.4951], tiles="Cartodbdark_matter", zoom_start=14)


    # print(backend + backend2)
    with row1_col1:

            if len(backend2) == 1:
                # with st.expander("See source code"):
                # with st.echo():
                # map_border = folium.Map(location=[13.72930616838845, 100.57522025302703], tiles="Cartodbdark_matter", zoom_start=11)
                # Add the district boundaries to the map
                folium.GeoJson(
                    districts,
                    style_function=style_function,
                    highlight_function=lambda x: {'weight': 3, 'color': '#3f999e', 'fillOpacity': 0.7 },
                    tooltip=folium.GeoJsonTooltip(fields=['dname', 'population'], labels=False, sticky=True)
                ).add_to(map_border)
                st_folium(map_border, width=-1400, height= 800, returned_objects=[])

            elif len(backend2) > 1:
                def plot_(data_map, num):
                    
                    color_list = ['#fa7202','#40eb34','#0ecced','#0ecced','#190eed','#ed0e0e','#ed0e0e']
                    for lat, lng, name in zip(data_map['lat'].astype(float), data_map['lng'].astype(float), data_map['name'] ):
                        folium.CircleMarker(
                            [lat, lng],
                            radius=5,
                            color= None, #'#fa7202',
                            fill=True,
                            popup=folium.Popup(name, max_width="100"),
                            fill_color= color_list[num], # '#fa7202',
                            fill_opacity=0.6,
                            parse_html=False
                        ).add_to(map_border)
                
                folium.GeoJson(
                    districts,
                    style_function=style_function0,
                    highlight_function=lambda x: {'weight': 3, 'color': '#3f999e', 'fillOpacity': 0 },
                    tooltip=folium.GeoJsonTooltip(fields=['dname'], labels=False, sticky=False)
                    ).add_to(map_border)
                for i, num in zip(backend2, range(len(backend2))):
                    # data_map = ''
                    # data_map = metro
                    if i == "Metro Train Station":
                        plot_(metro,num)
                    elif i == "Healthcare":
                        plot_(health,num)
                    elif i == "Market":
                        plot_(market,num)
                    elif i == "Department Store":
                        plot_(dep_sto,num)
                    elif i == "Fire Station":
                        plot_(fire,num)
                    elif i == "Police Station":
                        plot_(police,num)
                    elif i == "Community":
                        plot_(res,num)
                st_folium(map_border, width=-1400, height= 800, returned_objects=[])
            else:
                # with st.expander("See source code"):
                # with st.echo():
                folium.GeoJson(
                    districts,
                    style_function=style_function0,
                    highlight_function=lambda x: {'weight': 3, 'color': '#3f999e', 'fillOpacity': 0.7 },
                    tooltip=folium.GeoJsonTooltip(fields=['dname', 'population'], labels=False, sticky=True)
                ).add_to(map_border)

                # =========== RESIDENTIAL ===========
                for lat, lng, name in zip(res['lat'].astype(float), res['lng'].astype(float), res['name'] ):
                    folium.CircleMarker(
                        [lat, lng],
                        radius=3,
                        color= None, #'#fa7202',
                        fill=True,
                        popup=folium.Popup(name, max_width="100"),
                        fill_color='#fa7202',
                        fill_opacity=0.3,
                        parse_html=False
                    ).add_to(map_border)

                # =========== HEALTHCARE ===========
                for lat, lng, name in zip(health['lat'].astype(float), health['lng'].astype(float), health['name']):
                    folium.Circle([lat, lng],
                                radius=2500, # 5000 meters
                                color= None, #'#f100f5',
                                fill=True,
                                popup=folium.Popup(name, max_width="100"),
                                fill_color='#f100f5',
                                fill_opacity=0.5
                                ).add_to(map_border)
                st_folium(map_border, width=-1400, height= 800, returned_objects=[])



# add_points_from_xy(
#             cities,
#             x="longitude",
#             y="latitude",
#             color_column='region',
#             icon_names=['gear', 'map', 'leaf', 'globe'],
#             spin=True,
#             add_legend=True,
#         )
            
            
app()