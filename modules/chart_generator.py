import pandas as pd
import json
import os

def generate_chart_json(csv_path='data/tempo_aqi_risk.csv', output_json='static/aqi_chart_data.json'):
    """
    AQI risk skorlarını okur ve bar grafik için gerekli JSON yapısını oluşturur.
    Renkler AQI seviyelerine göre belirlenir.
    """
    if not os.path.exists(csv_path):
        print(f"❌ Risk CSV dosyası bulunamadı: {os.path.abspath(csv_path)}")
        return

    try:
        df = pd.read_csv(csv_path)

        required_cols = {'zone', 'risk_score'}
        if df.empty or not required_cols.issubset(df.columns):
            print("⚠️ CSV içeriği eksik. 'zone' ve 'risk_score' sütunları gerekli.")
            return

        # --- AQI ve Bölge Tanımları ---
        
        # Kuzey Amerika bölgeleri
        zone_labels_tr = {
            'Northwest': 'Kuzeybatı', 'North Central': 'Kuzey Orta', 'Northeast': 'Kuzeydoğu',
            'Southwest': 'Güneybatı', 'South Central': 'Güney Orta', 'Southeast': 'Güneydoğu'
        }
        zone_labels_en = {
            'Northwest': 'Northwest', 'North Central': 'North Central', 'Northeast': 'Northeast',
            'Southwest': 'Southwest', 'South Central': 'South Central', 'Southeast': 'Southeast'
        }

        # AQI seviyelerine göre renk ataması
        def get_aqi_color(score):
            if score <= 50: return '#00e400'  # İyi (Green)
            elif score <= 100: return '#ffff00'  # Orta (Yellow)
            elif score <= 150: return '#ff7e00'  # Hassas Gruplar (Orange)
            else: return '#ff0000'  # Sağlıksız (Red)
        
        # Her bir zonun ortalama risk skorunu al
        zone_scores = (
            df[['zone', 'risk_score']]
            .drop_duplicates(subset=['zone']) # Her zondan bir satır yeterli
            .groupby('zone', observed=False)
            .mean()
            .round(0) # AQI skorları tam sayı olmalıdır
            .reset_index()
            .sort_values('zone')
        )

        chart_data = {
            # Etiketleri Türkçe/İngilizce çevirme
            "labels_tr": [zone_labels_tr.get(z, z) for z in zone_scores['zone']],
            "labels_en": [zone_labels_en.get(z, z) for z in zone_scores['zone']],
            "values": zone_scores['risk_score'].tolist(),
            # Skorlara göre dinamik renk atama
            "colors": [get_aqi_color(s) for s in zone_scores['risk_score']],
            "title_tr": "TEMPO Bölgelerine Göre Ortalama AQI Skoru",
            "title_en": "Average AQI Score by TEMPO Zone",
            "max_value": 200 # Grafik limitini belirleyelim
        }

        # JSON dosyasını kaydet
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(chart_data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Çubuk grafik verisi oluşturuldu → {output_json}")

    except Exception as e:
        print(f"❌ Grafik JSON oluşturma hatası: {e}")

# Örnek Çağrı (app.py içinde): 
# from modules.chart_generator import generate_chart_json
# generate_chart_json(csv_path=RISK_PATH, output_json=JSON_PATH)