import pandas as pd
import json
import os

def generate_action_json(csv_path='data/tempo_aqi_risk.csv', output_json='static/aqi_action.json'):
    """
    AQI skorlarını sağlık risk seviyelerine dönüştürür ve eylem önerilerini içeren 
    JSON dosyasını Karar Destek Sistemi için oluşturur.
    """
    if not os.path.exists(csv_path):
        print(f"❌ Risk CSV dosyası bulunamadı: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    if 'zone' not in df.columns or 'risk_score' not in df.columns:
        print("❌ CSV'de 'zone' veya 'risk_score' sütunu eksik.")
        return

    # Sadece zon bazlı ortalama skoru al
    df = df[['zone', 'risk_score']].drop_duplicates(subset=['zone'])

    # --- AQI Sınıflandırma Mantığı ---
    def classify(score):
        if score <= 50: return 'İyi', 'Good'
        elif score <= 100: return 'Orta', 'Moderate'
        elif score <= 150: return 'Hassas Gruplar İçin Sağlıksız', 'Unhealthy for Sensitive Groups'
        else: return 'Sağlıksız', 'Unhealthy'

    # Risk Seviyelerine göre Eylem Haritası (Türkçe)
    action_map_tr = {
        'İyi': ['Açık hava aktiviteleri serbest ve önerilir.', 'Pencere/kapıları açmak güvenlidir.'],
        'Orta': ['Hassas gruplar (çocuklar, yaşlılar) uzun süreli açık hava aktivitesinden kaçınmalı.', 'Hava kalitesi izlenmeye devam edilmeli.'],
        'Hassas Gruplar İçin Sağlıksız': ['Astım/solunum problemi olanlar dışarı çıkmamalı.', 'Herkes yoğun efordan kaçınmalı.', 'Dışarıda N95/FFP2 maske kullanılması önerilir.'],
        'Sağlıksız': ['🚨 Zorunlu olmadıkça dışarı çıkmayın.', 'Dışarıda maske kullanın.', 'Pencere/kapıları kapalı tutun.', 'Hava temizleyici (air purifier) kullanılması tavsiye edilir.']
    }

    # Risk Seviyelerine göre Eylem Haritası (İngilizce)
    action_map_en = {
        'Good': ['Outdoor activities are permitted and encouraged.', 'Opening windows/doors is safe.'],
        'Moderate': ['Sensitive groups should limit prolonged outdoor exertion.', 'Air quality monitoring should continue.'],
        'Unhealthy for Sensitive Groups': ['Individuals with respiratory issues should stay indoors.', 'Everyone should limit strenuous activity.', 'Use of N95/FFP2 masks is recommended outdoors.'],
        'Unhealthy': ['🚨 Avoid going outdoors unless necessary.', 'Use a mask outside.', 'Keep windows and doors closed.', 'Air purifier use is advised indoors.']
    }

    # Kuzey Amerika bölgeleri
    zone_labels_tr = {
        'Northwest': 'Kuzeybatı', 'North Central': 'Kuzey Orta', 'Northeast': 'Kuzeydoğu',
        'Southwest': 'Güneybatı', 'South Central': 'Güney Orta', 'Southeast': 'Güneydoğu'
    }
    zone_labels_en = {
        'Northwest': 'Northwest', 'North Central': 'North Central', 'Northeast': 'Northeast',
        'Southwest': 'Southwest', 'South Central': 'South Central', 'Southeast': 'Southeast'
    }

    zones = []
    for _, row in df.iterrows():
        zone_key = row['zone']
        score_raw = row['risk_score']
        score = 0.0 if pd.isna(score_raw) else max(0, round(score_raw, 0)) # AQI tam sayı

        # Sınıflandırma
        level_tr, level_en = classify(score)

        name_tr = zone_labels_tr.get(zone_key, zone_key)
        name_en = zone_labels_en.get(zone_key, zone_key)

        # Eylemleri haritalama
        actions_tr = action_map_tr.get(level_tr, [])
        actions_en = action_map_en.get(level_en, [])

        zones.append({
            "name_tr": name_tr,
            "name_en": name_en,
            "risk_score": score,
            "level_tr": level_tr,
            "level_en": level_en,
            "actions_tr": actions_tr,
            "actions_en": actions_en
        })

    final_json = {"zones": zones}

    # JSON dosyasına yaz
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Karar destek JSON'u oluşturuldu → {output_json}")

# Örnek Çağrı (app.py içinde): 
# from modules.generate_action import generate_action_json
# generate_action_json(csv_path=RISK_PATH, output_json=JSON_PATH_ACTION)