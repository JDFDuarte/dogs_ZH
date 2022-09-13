import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
from collections import Counter

@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

dog_df_raw = load_data(path="./data/20200306_hundehalter.csv")
dog_df = deepcopy(dog_df_raw)

st.title("Dog Distribution per Kreis in the city of Zurich")
st.header("Data Exploration")


if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=dog_df)
    st.table(data=dog_df)


left_column, middle_column, right_column = st.columns([2, 1, 1])

districts = ["All"]+sorted(pd.unique(dog_df['STADTKREIS']))
dist = left_column.selectbox("Choose a District", districts)

if dist == "All":
    reduced_df = dog_df
else:
    reduced_df = dog_df[dog_df["STADTKREIS"] == dist]

# ____________________________________

with open('stzh.adm_stadtkreise_a.json') as json_file:
    locs_zh = json.load(json_file)

# count_alter = Counter()
# for item in df_mp["ALTER"]:
#     count_alter[item] += 1
# print(count_alter)


dogs_per_kreis = dog_df.groupby("STADTKREIS").size().reset_index(name='COUNT')
dogs_per_kreis.head()


fig = px.choropleth_mapbox(
    dogs_per_kreis,
    color="COUNT",
    geojson=locs_zh,
    locations="STADTKREIS",
    featureidkey="properties.name",
    center={"lat": 47.38, "lon": 8.54},
    zoom = 10,
    mapbox_style="open-street-map",
    opacity=0.6,
    labels={"STADTKREIS":"District",
           "COUNT":"Nr Dogs"},
    title="<b>Number of Dogs per District - Zurich</b>",
    color_continuous_scale="Purples",
)
fig.update_layout(margin={"r":0,"t":35,"l":0,"b":0},
                  font_color="black",
                  hoverlabel={"bgcolor":"grey",
                              "font_size":12},
                  title={"font_size":20,
                         "xanchor":"center", "x":0.38,
                        "yanchor":"bottom", "y":0.96}
                 )
fig.show()
