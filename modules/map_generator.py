import folium
import pandas as pd

def generate_map(csv_path, output_html):
    try:
        df = pd.read_csv(csv_path)
        m = folium.Map(location=[39.0, -95.0], zoom_start=4, tiles='CartoDB positron')

        color_map = {
            'Düşük': 'green',
            'Orta': 'orange',
            'Yüksek': 'red',
            'Çok Yüksek': 'darkred'
        }

        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=6,
                color=color_map.get(row['risk_level'], 'gray'),
                fill=True,
                fill_opacity=0.7,
                popup=f"AQI: {row['aqi']}<br>Risk: {row['risk_level']}"
            ).add_to(m)

        m.save(output_html)
        print(f"✅ Harita oluşturuldu: {output_html}")
    except Exception as e:
        print(f"❌ Harita oluşturma hatası: {e}")