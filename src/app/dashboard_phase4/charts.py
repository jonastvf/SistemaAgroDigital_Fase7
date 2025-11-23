import matplotlib.pyplot as plt
from pathlib import Path

PLOTS_DIR = Path("app/assets/plots")
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

def plot_humidity(df):
    plt.figure(figsize=(10, 4))
    plt.plot(df["timestamp"], df["humidity"])
    plt.title("Umidade ao longo do tempo")
    plt.xlabel("Tempo")
    plt.ylabel("Umidade (%)")
    plt.tight_layout()
    path = PLOTS_DIR / "humidity.png"
    plt.savefig(path)
    plt.close()
    return path.name


def plot_ph(df):
    plt.figure(figsize=(10, 4))
    plt.plot(df["timestamp"], df["ph"], color="orange")
    plt.title("Variação do pH")
    plt.xlabel("Tempo")
    plt.ylabel("pH")
    plt.tight_layout()
    path = PLOTS_DIR / "ph.png"
    plt.savefig(path)
    plt.close()
    return path.name


def plot_pump(df):
    plt.figure(figsize=(10, 4))
    plt.plot(df["timestamp"], df["pump_on"], color="green")
    plt.title("Bomba ligada/desligada")
    plt.xlabel("Tempo")
    plt.ylabel("Estado (0/1)")
    plt.tight_layout()
    path = PLOTS_DIR / "pump.png"
    plt.savefig(path)
    plt.close()
    return path.name
