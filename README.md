
## 🌪️ StormSentinel: Air Quality & Disaster Risk Intelligence Platform

**NASA Space Apps Challenge 2025 Submission**  
Challenge: *Earth’s Atmosphere*  
Team: Selim CNR

---

### 🚀 Overview

**StormSentinel** is a modular, multilingual decision-support platform that transforms NASA atmospheric data into actionable insights for disaster risk and public health. It processes real-time NO₂ data from the TEMPO mission, calculates AQI scores, and maps regional risk zones across North America. The system generates interactive maps, charts, and localized action recommendations to empower communities and responders.

---

### 🎯 What It Does

- ✅ Extracts NO₂ vertical column data from NASA TEMPO HDF5/NetCDF files  
- ✅ Calculates AQI scores using EPA-inspired thresholds  
- ✅ Classifies regions into North American zones  
- ✅ Generates interactive risk maps and bar charts  
- ✅ Provides zone-specific action recommendations  
- ✅ Supports multilingual UI and scalable architecture

---

### 🧠 Technologies Used

- **Languages**: Python, JavaScript, HTML/CSS  
- **Frameworks**: Flask, Bootstrap, Leaflet.js  
- **Libraries**: Pandas, NumPy, h5py, NetCDF4  
- **Data Sources**:  
  - [NASA TEMPO NO₂ Data](https://www.earthdata.nasa.gov/sensors/tempo)  
  - [MODIS Fire/Aerosol Products](https://modis.gsfc.nasa.gov/data/dataprod/mod14.php)  
  - [GPM Precipitation Data](https://gpm.nasa.gov/data)  
  - [SEDAC Population Density](https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density)

---

### 🌍 Why It Matters

StormSentinel bridges the gap between complex scientific data and public action. By making air quality intelligence understandable and usable, it empowers local governments, health agencies, and citizens to respond faster and smarter to environmental risks. Its modular design allows global adaptation and future dataset integration.

---

### 📦 Project Structure

```
├── app.py                 # Flask web server
├── tempo_reader.py        # HDF5/NetCDF data extraction
├── aqi_calculator.py      # AQI scoring and zonal risk logic
├── map_generator.py       # Leaflet-based map rendering
├── chart_generator.py     # Bar chart JSON output
├── action_generator.py    # Decision-support recommendations
├── /data                  # Input/output CSV files
├── /static                # Icons, styles, assets
├── /templates             # HTML templates
```

---

### 📽️ Demo

Watch the 30-second demo:  
[https://drive.google.com/file/d/your-demo-id/view](https://drive.google.com/file/d/your-demo-id/view)

---

### 🤖 AI Usage

AI tools were used to assist in code generation, UI/UX planning, and strategic presentation scripting. All AI-generated content was reviewed and manually integrated. No NASA branding was used in AI-generated assets.

---

### 📄 License

This project is open-source under the MIT License.  
All NASA data used is publicly available and properly cited.

