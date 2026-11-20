from pathlib import Path
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ecommerce_orders.csv"
OUT = ROOT / "outputs"
MODEL = ROOT / "models" / "return_model.joblib"
DB = ROOT / "ecommerce_returns.db"

def run_pipeline():
    OUT.mkdir(exist_ok=True)
    (ROOT / "models").mkdir(exist_ok=True)
    df = pd.read_csv(DATA)
    df = df.drop_duplicates(subset=["Order_ID"]).copy()
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    numeric = ["Product_Price","Quantity","Discount_Percent","Delivery_Days","Customer_Rating","Order_Value"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())
    df["Product_Category"] = df["Product_Category"].fillna("Unknown")
    df["Payment_Method"] = df["Payment_Method"].fillna("Unknown")
    df["Shipping_Type"] = df["Shipping_Type"].fillna("Unknown")
    df["Is_Returned"] = df["Is_Returned"].astype(int)
    df.to_csv(OUT / "cleaned_orders.csv", index=False)

    # Derived fields for Power BI
    df["Order_Month"] = df["Order_Date"].dt.strftime("%Y-%m")
    df["Returned_Value"] = np.where(df["Is_Returned"] == 1, df["Order_Value"], 0)
    df["Return_Flag"] = np.where(df["Is_Returned"] == 1, "Returned", "Not Returned")
    df.to_csv(OUT / "powerbi_orders.csv", index=False)

    # SQL database
    db_df = df.copy()
    db_df["Order_Date"] = db_df["Order_Date"].dt.strftime("%Y-%m-%d")
    with sqlite3.connect(DB) as conn:
        db_df.to_sql("orders", conn, if_exists="replace", index=False)
        pd.read_sql_query("SELECT COUNT(*) AS total_orders FROM orders", conn).to_csv(OUT/"sql_check.csv", index=False)

    # EDA exports and charts
    summary = df.groupby("Product_Category").agg(
        Total_Orders=("Order_ID","count"),
        Returned_Orders=("Is_Returned","sum"),
        Order_Value=("Order_Value","sum"),
        Returned_Value=("Returned_Value","sum")
    ).reset_index()
    summary["Return_Rate_Pct"] = (summary.Returned_Orders/summary.Total_Orders*100).round(2)
    summary.to_csv(OUT/"category_summary.csv", index=False)

    monthly = df.groupby("Order_Month").agg(
        Total_Orders=("Order_ID","count"), Returned_Orders=("Is_Returned","sum"),
        Sales=("Order_Value","sum"), Returned_Value=("Returned_Value","sum")
    ).reset_index()
    monthly["Return_Rate_Pct"] = (monthly.Returned_Orders/monthly.Total_Orders*100).round(2)
    monthly.to_csv(OUT/"monthly_summary.csv", index=False)

    reason = df[df.Is_Returned == 1].groupby("Return_Reason").size().reset_index(name="Return_Count")
    reason.to_csv(OUT/"return_reason_summary.csv", index=False)

    sns.set_theme()
    plt.figure(figsize=(9,5))
    plt.bar(summary["Product_Category"], summary["Return_Rate_Pct"])
    plt.xticks(rotation=25, ha="right"); plt.ylabel("Return Rate (%)")
    plt.title("Return Rate by Product Category"); plt.tight_layout()
    plt.savefig(OUT/"category_return_rate.png", dpi=160); plt.close()

    plt.figure(figsize=(10,5))
    plt.plot(monthly["Order_Month"], monthly["Return_Rate_Pct"], marker="o")
    plt.xticks(rotation=45); plt.title("Monthly Return Rate Trend"); plt.tight_layout()
    plt.savefig(OUT/"monthly_return_trend.png", dpi=160); plt.close()

    # ML: exclude post-outcome columns (Return_Reason, Is_Returned)
    features = ["Product_Category","Product_Price","Quantity","Discount_Percent",
                "Payment_Method","Shipping_Type","Delivery_Days","Customer_Rating"]
    X, y = df[features], df["Is_Returned"]
    cat_cols = ["Product_Category","Payment_Method","Shipping_Type"]
    num_cols = [c for c in features if c not in cat_cols]
    pre = ColumnTransformer([
        ("cat", Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),
                          ("onehot",OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
        ("num", Pipeline([("imputer",SimpleImputer(strategy="median")),
                          ("scale",StandardScaler())]), num_cols)
    ])
    model = Pipeline([("preprocess",pre),("classifier",RandomForestClassifier(
        n_estimators=250, max_depth=10, min_samples_leaf=3, class_weight="balanced",
        random_state=42))])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.20, random_state=42, stratify=y)
    model.fit(X_train,y_train)
    pred = model.predict(X_test)
    proba = model.predict_proba(X_test)[:,1]
    (OUT/"model_metrics.txt").write_text(
        "Classification report\n"+classification_report(y_test,pred,zero_division=0)+
        f"ROC-AUC: {roc_auc_score(y_test,proba):.4f}\n"+
        "Confusion matrix:\n"+str(confusion_matrix(y_test,pred)), encoding="utf-8")
    joblib.dump({"model":model,"features":features}, MODEL)

    # Prediction output with low/medium/high risk labels
    sample = X_test.copy()
    sample["Return_Probability"] = model.predict_proba(X_test)[:,1]
    sample["Risk_Level"] = pd.cut(sample.Return_Probability,
        bins=[-0.001,.30,.60,1.0], labels=["Low","Medium","High"])
    sample.to_csv(OUT/"sample_return_predictions.csv", index=False)

    print("Pipeline completed successfully.")
    print(f"Database: {DB}")
    print(f"Power BI data: {OUT/'powerbi_orders.csv'}")
    print(f"Model metrics: {OUT/'model_metrics.txt'}")

if __name__ == "__main__":
    run_pipeline()
