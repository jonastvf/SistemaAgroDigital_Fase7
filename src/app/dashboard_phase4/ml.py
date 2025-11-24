import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from pathlib import Path

PLOTS_DIR = Path("app/assets/plots")

def forecast_humidity(df):
    df = df.copy()
    df["t"] = np.arange(len(df))

    model = LinearRegression()
    model.fit(df[["t"]], df["humidity"])

    future_t = np.arange(len(df), len(df) + 10).reshape(-1, 1)
    prediction = model.predict(future_t)

    # Plot
    plt.figure(figsize=(10, 4))
    plt.plot(prediction, marker="o")
    plt.title("Previsão de umidade (10 passos)")
    plt.xlabel("Passos futuros")
    plt.ylabel("Umidade prevista")
    plt.tight_layout()

    path = PLOTS_DIR / "forecast.png"
    plt.savefig(path)
    plt.close()

    return path.name, prediction.tolist()
