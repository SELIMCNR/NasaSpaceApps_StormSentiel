import h5py
import pandas as pd
import numpy as np
import os
"""
def extract_tempo_data(hdf_path='data/temp.nc', output_csv='data/tempo_no2.csv'):
    try:
        with h5py.File(hdf_path, 'r') as f:
            print("📦 Dosya açıldı:", list(f.keys()))

            if 'product' in f and 'vertical_column_troposphere' in f['product'] and \
               'latitude' in f and 'longitude' in f:
                
                raw = f['product']['vertical_column_troposphere'][...]  # shape: (1, lat, lon)
                lat = f['latitude'][...]
                lon = f['longitude'][...]

                print("📐 raw shape:", raw.shape)
                print("🧭 lat:", len(lat), "| lon:", len(lon))

                no2 = np.squeeze(raw)  # shape: (lat, lon)
                no2 = no2.T            # shape: (lon, lat)
                print("📐 no2 shape (transposed):", no2.shape)

            else:
                print("❌ Beklenen veri alanları bulunamadı.")
                return None

            records = []
            for i in range(len(lat)):
                for j in range(len(lon)):
                    value = no2[j, i]  # dikkat: [lon, lat]
                    if np.isfinite(value):
                        records.append({
                            'latitude': round(lat[i], 4),
                            'longitude': round(lon[j], 4),
                            'no2': round(float(value), 4)
                        })

            if not records:
                print("⚠️ Veri boş, kayıt oluşturulamadı.")
                return None

            df = pd.DataFrame(records)
            df.to_csv(output_csv, index=False)
            print(f"✅ {len(df)} kayıt yazıldı → {output_csv}")
            return output_csv

    except Exception as e:
        print(f"❌ TEMPO veri okuma hatası: {e}")
        return None
        
        """
def extract_tempo_data(hdf_path='data/temp.nc', output_csv='data/tempo_no2.csv'):
    try:
        with h5py.File(hdf_path, 'r') as f:
            print("📦 Dosya açıldı:", list(f.keys()))

            if 'product' in f and 'vertical_column_troposphere' in f['product'] and \
               'latitude' in f and 'longitude' in f:
                
                raw = f['product']['vertical_column_troposphere'][...]  # (1, lat, lon)
                lat = f['latitude'][...]  # (lat,)
                lon = f['longitude'][...]  # (lon,)

                no2 = np.squeeze(raw).T  # (lon, lat)
                print("📐 no2 shape:", no2.shape)

            else:
                print("❌ Beklenen veri alanları bulunamadı.")
                return None

            # Vektörel filtreleme
            mask = np.isfinite(no2)
            jj, ii = np.where(mask)  # j: lon index, i: lat index

            # NumPy ile kayıt üretimi
            lat_vals = lat[ii]
            lon_vals = lon[jj]
            no2_vals = no2[jj, ii]

            df = pd.DataFrame({
                'latitude': np.round(lat_vals, 4),
                'longitude': np.round(lon_vals, 4),
                'no2': np.round(no2_vals.astype(float), 4)
            })

            df.to_csv(output_csv, index=False)
            print(f"✅ {len(df)} kayıt yazıldı → {output_csv}")
            return output_csv

    except Exception as e:
        print(f"❌ TEMPO veri okuma hatası: {e}")
        return None        