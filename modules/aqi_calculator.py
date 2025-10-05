import pandas as pd
import os
import numpy as np

# 📁 Dosya yolları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'tempo_no2.csv')           # NO2 verisi
RISK_PATH = os.path.join(BASE_DIR, 'data', 'tempo_aqi_risk.csv')     # AQI skorları

# 📍 Kuzey Amerika zonlama fonksiyonu
def define_us_region(lat, lon):
    if 45 <= lat <= 55 and -130 <= lon <= -100:
        return 'Northwest'
    elif 40 <= lat <= 50 and -100 < lon <= -70:
        return 'North Central'
    elif 40 <= lat <= 50 and -70 < lon <= -40:
        return 'Northeast'
    elif 30 <= lat < 45 and -120 <= lon <= -100:
        return 'Southwest'
    elif 10 <= lat < 40 and -100 < lon <= -70:
        return 'South Central'
    elif 25 <= lat < 40 and -70 < lon <= -40:
        return 'Southeast'
    else:
        return 'Outside TEMPO Area'

# 🌫️ NO2 → AQI dönüşüm fonksiyonu (EPA eşiklerine yakınlaştırılmış)
def calculate_aqi_score(no2_concentration):
    if no2_concentration < 1.5e16:
        return int(no2_concentration / 1.5e16 * 50)  # Good
    elif no2_concentration < 2.8e16:
        return int(50 + (no2_concentration - 1.5e16) / (2.8e16 - 1.5e16) * 50)  # Moderate
    elif no2_concentration < 1.0e17:
        return int(100 + (no2_concentration - 2.8e16) / (1.0e17 - 2.8e16) * 50)  # Unhealthy for Sensitive Groups
    else:
        return int(150 + (no2_concentration - 1.0e17) / 1.0e17 * 100)  # Unhealthy+

# 🔴 Risk seviyesini kategorik olarak belirleme
def risk_level(score):
    if score <= 50: return 'Low'
    elif score <= 100: return 'Moderate'
    elif score <= 150: return 'High'
    else: return 'Very High'

# 🧮 Ana AQI hesaplama fonksiyonu
def calculate_aqi(csv_path=CSV_PATH, output_csv=RISK_PATH):
    if not os.path.exists(csv_path):
        print(f"❌ CSV dosyası bulunamadı: {csv_path}")
        return None

    df = pd.read_csv(csv_path)

    # Sütun adını dönüştür (uyumluluk için)
    if 'no2' in df.columns:
        df.rename(columns={'no2': 'NO2_column'}, inplace=True)

    required_columns = {'latitude', 'longitude', 'NO2_column'}
    if df.empty:
        print("⚠️ CSV dosyası boş.")
        return None
    if not required_columns.issubset(df.columns):
        print(f"⚠️ CSV sütunları eksik. Gerekli sütunlar: {required_columns}")
        print(f"📄 Mevcut sütunlar: {list(df.columns)}")
        return None

    # 1️⃣ AQI skoru hesapla
    df['AQI_score'] = df['NO2_column'].apply(calculate_aqi_score)

    # 2️⃣ Zonları ata
    df['zone'] = df.apply(lambda row: define_us_region(row['latitude'], row['longitude']), axis=1)

    # 3️⃣ TEMPO kapsama dışı veriyi filtrele
    df = df[df['zone'] != 'Outside TEMPO Area'].copy()

    # 4️⃣ Zon bazlı ortalama risk skoru
    zone_risk = df.groupby('zone', observed=False)['AQI_score'].mean().round(0).reset_index()
    zone_risk.columns = ['zone', 'risk_score']

    # 5️⃣ Tüm verilere zon risk skorunu ekle
    df = df.merge(zone_risk, on='zone', how='left')

    # 6️⃣ Risk seviyesini kategorik olarak ekle
    df['risk_level'] = df['risk_score'].apply(risk_level)

    # 7️⃣ Harita modülü için 'aqi' sütonunu ekle
    df.rename(columns={'AQI_score': 'aqi'}, inplace=True)

    # 8️⃣ Sadece gerekli sütunları kaydet
    df = df[['latitude', 'longitude', 'NO2_column', 'zone', 'aqi', 'risk_score', 'risk_level']]

    df.to_csv(output_csv, index=False)
    print(f"✅ AQI Risk Skoru hesaplandı ve {output_csv} dosyasına kaydedildi.")
    return output_csv