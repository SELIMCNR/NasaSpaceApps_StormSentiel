import os
import time
import pandas as pd
import json
from flask import Flask, render_template, redirect, url_for, send_file
import h5py
 
# --- TEMPO'ya Özel Yeni Modüller ---
from modules.tempo_reader import extract_tempo_data
from modules.aqi_calculator import calculate_aqi_score,calculate_aqi
from modules.map_generator import generate_map
from modules.chart_generator import generate_chart_json
from modules.generate_action import generate_action_json


app = Flask(__name__)

# --- Yeni Dosya Yolları (TEMPO AQI Odaklı) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# NOT: Artık tek bir örnek HDF5 dosyası kullanılmayacak, veri canlı çekilecek.
# DATA_PATH = os.path.join(BASE_DIR, 'data', 'gpm_sample.HDF5') # Bu satır silindi.

CSV_PATH = os.path.join(BASE_DIR, 'data', 'tempo_no2.csv') # NO2 verisi (Lat/Lon/NO2_column)
RISK_PATH = os.path.join(BASE_DIR, 'data', 'tempo_aqi_risk.csv') # AQI skorları
MAP_PATH = os.path.join(BASE_DIR, 'visuals', 'aqi_map.html') # Yeni Harita
JSON_PATH = os.path.join(BASE_DIR, 'static', 'aqi_chart_data.json') # Grafik Verisi
JSON_PATH_ACTION = os.path.join(BASE_DIR, 'static', 'aqi_action.json') # Karar Destek Verisi
PDF_PATH = os.path.join(BASE_DIR, 'static', 'aqi_report.pdf') # Yeni PDF Yolu
CHARTH_PATH=os.path.join(BASE_DIR, 'visuals', 'charth.html') # Yeni Harita
# --- Yeni Dosya Yolları ---
NC_PATH = os.path.join(BASE_DIR, 'data', 'temp.nc') 

# GPM/MODIS ile ilgili tüm eski rotalar (run_all, modis_panel, combined_panel) kaldırıldı.
@app.route('/')
def index():
    return render_template('index.html')

# Ana Panel Rotası (Eski storm_panel, yeni AQI panelini temsil eder)
@app.route('/aqi_panel')
def aqi_panel():
    # Veri başarıyla işlendiyse, ortalama risk skorunu alıp panele gönderelim.
    try:
        df = pd.read_csv(RISK_PATH)
        # Bütün zonların ortalama AQI risk skoru
        avg_aqi = df['risk_score'].mean().round(0)
    except:
        avg_aqi = "N/A" # Veri henüz çekilmediyse

    return render_template('storm_panel.html', avg_aqi=avg_aqi) # storm_panel.html'i AQI verisiyle doldurun

# Harita ve Grafik Rotası
@app.route('/aqi_map_graph_panel')
def aqi_map_graph_panel():
    return render_template('storm_map_graph_panel.html')

# Harita ve Grafik dosyaları (Yollar güncellendi)
@app.route('/aqi_map')
def aqi_map():
    return send_file(MAP_PATH) if os.path.exists(MAP_PATH) else "❌ Harita dosyası bulunamadı. Veri güncellemeyi deneyin."

@app.route('/aqi_chart')
def aqi_chart():
    return send_file(CHARTH_PATH) if os.path.exists(CHARTH_PATH) else "❌ Grafik dosyası bulunamadı. Veri güncellemeyi deneyin."

# Karar Destek Rotası (Yol güncellendi)
@app.route('/decision_support')
def decision_support():
    try:
        with open(JSON_PATH_ACTION, 'r', encoding='utf-8') as f:
            data = json.load(f)
        zones = data.get("zones", [])
        return render_template('decision_support.html', zones=zones)
    except Exception as e:
        return f"<h4>❌ Karar destek verisi yüklenemedi: {str(e)}</h4>"

@app.route('/update_data')
def update_data():
    start = time.time()
    try:
        print("🚀 TEMPO AQI veri akışı başlatıldı...")

        # 1. TEMPO verisini çek ve CSV'ye yaz
     #  tempo_csv = extract_tempo_data(hdf_path=NC_PATH, output_csv=CSV_PATH)
      #  if not tempo_csv:
      #      return "<h4>❌ TEMPO veri çekme/işleme başarısız. Dosya yapısını veya earthaccess girişini kontrol edin.</h4>"

        # 2. AQI skorlarını hesapla
        risk_csv = calculate_aqi(csv_path=CSV_PATH, output_csv=RISK_PATH)
        if not risk_csv:
            return "<h4>❌ AQI hesaplama başarısız. Veri formatını veya eşik değerlerini kontrol edin.</h4>"

        # 3. Görsel ve karar destek dosyalarını oluştur
        generate_map(csv_path=RISK_PATH, output_html=MAP_PATH)
        generate_chart_json(csv_path=RISK_PATH, output_json=JSON_PATH)
        generate_action_json(csv_path=RISK_PATH, output_json=JSON_PATH_ACTION)

        # (İsteğe bağlı) PDF raporu oluştur
        # generate_pdf_report(RISK_PATH, output_path=PDF_PATH)

        duration = round(time.time() - start, 2)
        print(f"✅ TEMPO AQI veri akışı tamamlandı ({duration} saniye).")
        return redirect(url_for('aqi_panel'))

    except Exception as e:
        print(f"❌ Güncelleme hatası: {e}")
        return f"<h4>❌ Güncelleme sırasında hata oluştu:<br>{str(e)}</h4>"
# Diğer rotaları (data_sources, debug_paths) koruyoruz
@app.route('/data_sources')
def data_sources():
    return render_template('data_sources.html')

@app.route('/debug')
def debug_paths():
    return f"""
    📁 CSV_PATH: {CSV_PATH} → {os.path.exists(CSV_PATH)}<br>
    📁 RISK_PATH: {RISK_PATH} → {os.path.exists(RISK_PATH)}<br>
    📁 MAP_PATH: {MAP_PATH} → {os.path.exists(MAP_PATH)}<br>
    📁 CHART_PATH: {JSON_PATH} → {os.path.exists(JSON_PATH)}<br>
    📁 ACTION_PATH: {JSON_PATH_ACTION} → {os.path.exists(JSON_PATH_ACTION)}<br>
    """

if __name__ == '__main__':
    # Flask ayarları: 'modules' klasörünün varlığını kontrol edin ve yoksa oluşturun.
    os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'visuals'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'static'), exist_ok=True)
    
    app.run(debug=True, use_reloader=False)