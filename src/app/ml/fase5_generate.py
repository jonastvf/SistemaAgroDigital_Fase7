import os
import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "plots" /"fase5"
DATA_PATH = BASE_DIR / "ml" / "crop_yield.csv"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH, sep=";")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("(", "")
    .str.replace(")", "")
    .str.replace("-", "")
)

plt.figure(figsize=(8, 5))
df["yield"].hist(bins=20, color="skyblue", edgecolor="black")
plt.title("Distribuição do Rendimento")
plt.xlabel("Rendimento (t/ha)")
plt.ylabel("Frequência")
plt.savefig(ASSETS_DIR / "eda_distribution.png")
plt.close()

plt.figure(figsize=(8, 5))
df.boxplot(column=["yield"])
plt.title("Boxplot – Rendimento")
plt.savefig(ASSETS_DIR / "eda_boxplot.png")
plt.close()

numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()

plt.figure(figsize=(10, 8))
plt.matshow(corr, cmap="coolwarm", fignum=1)
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.colorbar()
plt.title("Correlação das Variáveis", pad=20)
plt.savefig(ASSETS_DIR / "eda_correlation.png")
plt.close()

cluster_features = numeric_df[["precipitation_mm_day1", "temperature_at_2_meters_c", "yield"]]

kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto")
df["cluster"] = kmeans.fit_predict(cluster_features)

plt.figure(figsize=(8, 6))
plt.scatter(df["temperature_at_2_meters_c"], df["yield"], c=df["cluster"], cmap="viridis")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Rendimento (t/ha)")
plt.title("Clusters – Temperatura x Rendimento")
plt.savefig(ASSETS_DIR / "clusters.png")
plt.close()

X = numeric_df.drop(columns=["yield"])
y = df["yield"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "LinearRegression": LinearRegression(),
    "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42),
    "KNN": KNeighborsRegressor(n_neighbors=5),
    "SVR": SVR(kernel="rbf"),
}

metrics = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, pred)
    mse = mean_squared_error(y_test, pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, pred)
    metrics[name] = {
        "MAE": float(mae),
        "MSE": float(mse),
        "RMSE": float(rmse),
        "R2": float(r2),
    }

plt.figure(figsize=(10, 6))
model_names = list(metrics.keys())
rmse_values = [metrics[m]["RMSE"] for m in model_names]
plt.bar(model_names, rmse_values, color="salmon")
plt.ylabel("RMSE")
plt.title("Comparação de Modelos – RMSE")
plt.savefig(ASSETS_DIR / "model_comparison.png")
plt.close()

output = {
    "status": "success",
    "summary": {
        "dataset_rows": len(df),
        "best_model": min(metrics, key=lambda m: metrics[m]["RMSE"]),
    },
    "metrics": metrics,
    "charts": {
        "distribution": "eda_distribution.png",
        "boxplot": "eda_boxplot.png",
        "correlation": "eda_correlation.png",
        "clusters": "clusters.png",
        "model_comparison": "model_comparison.png",
    },
}

with open(ASSETS_DIR / "results.json", "w") as f:
    json.dump(output, f, indent=4)

print("Modelos treinados e arquivos gerados com sucesso!")
