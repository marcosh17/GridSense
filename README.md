# ⚡ GridSense

GridSense is a modular backend system for real-time extraction, normalization and prediction of energy data in Spain.  
The project is designed for energy forecasting, intelligent monitoring, and estimating environmental impact from real electricity demand.

> Early version (Phase 1): Data extraction and CSV storage only.

---

## 🌐 APIs Used

- **Red Eléctrica de España (ESIOS API)** – hourly electricity demand  
  → https://www.esios.ree.es/es/api-documentation

- **PVGIS API** – solar irradiance and photovoltaic simulation data  
  → https://re.jrc.ec.europa.eu/pvg_tools/en/

- **OpenWeatherMap API** – weather data 
  → https://openweathermap.org/api

- **Our World in Data (CO₂)** – emission factors and global stats  
  → https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions

---

## 🚀 Getting Started

1. Clone the repository:

```
git clone https://github.com/your-username/GridSense.git
cd GridSense
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create a `.env` file with your API token:

```
ESIOS_TOKEN=your_ree_api_token
```

4. Run the extractor script:

```
python app/main.py
```

This will generate a CSV with the latest demand data in `data/consumo_ree.csv`.

---

## 📦 Commit Convention

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) format:

<type>(<scope>): <short description>

**Examples:**

- feat(ree): extract and store hourly demand data from REE
- fix(config): correct token loading from .env
- docs(readme): add project introduction and usage guide

**Valid types:** feat, fix, docs, style, refactor, test, chore

> Never commit sensitive files like `.env`. It is ignored by default.

---

## 🧠 Future Plans

- Add data normalization and resampling by time and region  
- Implement energy demand forecasting (Prophet, LSTM)  
- Include environmental impact equivalence in CO₂  
- Build an API layer with FastAPI to serve predictions  
- Deploy a real-time dashboard

---

© GridSense · MIT License