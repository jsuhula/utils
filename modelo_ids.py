import pandas as pd
from sklearn.ensemble import IsolationForest
import warnings

warnings.filterwarnings('ignore')

def ejecutar_ids():
    # 1. Cargar los datos extraídos
    try:
        df_normal = pd.read_csv('normal.csv')
        df_ataque = pd.read_csv('ataque.csv')
    except FileNotFoundError:
        print("Error: No se encontraron los archivos CSV.")
        return

    # 2. Separar las características (X) de las IPs 
    X_normal = df_normal[['pps', 'puertos', 'bytes']]
    X_ataque = df_ataque[['pps', 'puertos', 'bytes']]

    # === FASE 4: Entrenamiento del Modelo ===
    # Utilizamos Isolation Forest con una contaminación del 10% (0.1) como sugiere la guía
    modelo = IsolationForest(contamination=0.1, random_state=42)
    modelo.fit(X_normal)

    # === FASE 5: Detección de Anomalías
    predicciones = modelo.predict(X_ataque)

    # Mapear los resultados (-1 y 1) a texto legible
    df_ataque['resultado'] = ['normal' if x == 1 else 'anomalia' for x in predicciones]

    # Mostrar resultados generales
    print("=== RESULTADOS SOBRE ataque.csv ===")
    print(df_ataque.to_string())

    # Filtrar y mostrar solo las anomalías
    print("\n=== SOLO ANOMALIAS ===")
    anomalias = df_ataque[df_ataque['resultado'] == 'anomalia']
    print(anomalias.to_string())
    print("\n")

    for index, fila in anomalias.iterrows():
        print(f"[ALERTA] IP {fila['ip']} comportamiento anómalo")

if __name__ == "__main__":
    ejecutar_ids()