import pandas as pd
from pathlib import Path
from app.config import LOCATIONS

def combine_csvs(source: str):
    """
    Combina todos los CSV por ciudad de una fuente (pvgis o openmeteo) en un solo archivo.
    """
    print(f"📦 Combinando CSVs de todas las ciudades para {source}...")
    all_data = []

    for city in LOCATIONS:
        path = Path("data") / city.lower() / "raw" / f"{source}_{city.lower()}_2005_2020.csv"
        if path.exists():
            df = pd.read_csv(path)
            all_data.append(df)
        else:
            print(f"⚠️ Archivo no encontrado: {path}")

    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        output_path = Path("data") / "raw_data" / f"{source}_all_cities.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        combined.to_csv(output_path, index=False)
        print(f"✅ Datos combinados guardados en: {output_path}")
    else:
        print("❌ No se encontraron archivos para combinar.")

if __name__ == "__main__":
    combine_csvs("pvgis")
    combine_csvs("openmeteo")