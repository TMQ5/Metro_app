import streamlit as st
import networkx as nx
import folium
from streamlit_folium import st_folium

# محطات تجريبية
stations = {
    "العليا": {"line": "أزرق", "coords": (24.713, 46.675)},
    "البطحاء": {"line": "أزرق", "coords": (24.700, 46.680)},
    "الحائر": {"line": "أزرق", "coords": (24.690, 46.685)},
    "الملك عبدالله": {"line": "أحمر", "coords": (24.750, 46.730)},
    "الندوة": {"line": "أحمر", "coords": (24.740, 46.735)},
    "اليرموك": {"line": "أحمر", "coords": (24.730, 46.740)},
    "المدينة": {"line": "برتقالي", "coords": (24.640, 46.700)},
    "الأمير سعد": {"line": "برتقالي", "coords": (24.630, 46.705)},
    "طويق": {"line": "برتقالي", "coords": (24.620, 46.710)}
}

# إنشاء الرسم البياني
G = nx.Graph()
for name, data in stations.items():
    G.add_node(name, coords=data["coords"])

edges = [
    ("العليا", "البطحاء"), ("البطحاء", "الحائر"),
    ("الملك عبدالله", "الندوة"), ("الندوة", "اليرموك"),
    ("المدينة", "الأمير سعد"), ("الأمير سعد", "طويق")
]

for u, v in edges:
    c1, c2 = stations[u]["coords"], stations[v]["coords"]
    distance = ((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)**0.5
    G.add_edge(u, v, weight=distance)

st.title("🚇 نظام مسارات مترو الرياض")

start = st.selectbox("اختر محطة البداية:", list(stations.keys()))
end = st.selectbox("اختر محطة الوصول:", list(stations.keys()))

if start and end and start != end:
    if nx.has_path(G, start, end):
        path = nx.shortest_path(G, source=start, target=end, weight="weight")
        st.success(f"أقصر مسار من {start} إلى {end} هو: {' → '.join(path)}")

        m = folium.Map(location=[24.7136, 46.6753], zoom_start=12)

        for station, data in stations.items():
            folium.CircleMarker(
                location=data["coords"],
                radius=5,
                color="blue" if station in path else "gray",
                fill=True,
                popup=station
            ).add_to(m)

        coords = [stations[pt]["coords"] for pt in path]
        folium.PolyLine(coords, color="blue", weight=5).add_to(m)

        st_folium(m, width=700, height=500)
    else:
        st.error(f"لا يوجد مسار متصل بين {start} و {end}.")
else:
    st.warning("يرجى اختيار محطتين مختلفتين.")
