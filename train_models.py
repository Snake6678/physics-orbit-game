"""Model training utilities for stock classification.

This script downloads historical price data for a set of tickers and trains a
binary classifier that predicts whether the price will be higher three trading
days in the future.  The trained models along with preprocessing objects are
saved to the ``models`` directory.
"""

from __future__ import annotations

import os
from datetime import datetime

import joblib
import pandas as pd
import yfinance as yf
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import GradientBoostingClassifier, StackingClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Tickers used for training
TICKERS = [
    "SPY",
    "AAPL",
    "MSFT",
    "TSLA",
    "GOOGL",
    "NVDA",
    "AMZN",
    "META",
    "JPM",
    "XOM",
    "V",
]


def download_data(ticker: str) -> pd.DataFrame:
    """Download adjusted close prices for ``ticker`` and reference ETFs."""
    end = datetime.today().strftime("%Y-%m-%d")
    start = "2010-01-01"

    def get_price(symbol: str) -> pd.Series:
        df = yf.download(symbol, start=start, end=end, progress=False)
        if "Adj Close" in df.columns:
            return df["Adj Close"].rename(symbol)
        if "Close" in df.columns:
            return df["Close"].rename(symbol)
        raise ValueError(f"No price data found for {symbol}")

    try:
        main = get_price(ticker)
        tlt = get_price("TLT")
        gld = get_price("GLD")
    except Exception as exc:  # pragma: no cover - network call
        raise ValueError(f"Failed to download data for {ticker}: {exc}") from exc

    return pd.concat([main, tlt, gld], axis=1).dropna()


def engineer_features(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Create percentage change features and a three-day forward target."""
    df = df.pct_change().dropna()
    df["target"] = (df[ticker].shift(-3) > df[ticker]).astype(int)
    return df.dropna()


def train_model_for_ticker(ticker: str) -> None:
    """Train and save a model for ``ticker``."""
    print(f"Training model for {ticker}...")

    try:
        prices = download_data(ticker)
        features = engineer_features(prices, ticker)
        X = features.drop("target", axis=1)
        y = features["target"]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        smote = SMOTE()
        X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

        xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42)
        gb = GradientBoostingClassifier(random_state=42)
        lr = LogisticRegression(max_iter=1000, random_state=42)

        estimators = [("xgb", xgb), ("gb", gb)]
        stacked = StackingClassifier(estimators=estimators, final_estimator=lr, cv=5)
        stacked.fit(X_resampled, y_resampled)

        selector = SelectFromModel(estimator=stacked, threshold="mean", prefit=True)
        X_selected = selector.transform(X_resampled)

        final_model = LogisticRegression(max_iter=1000)
        final_model.fit(X_selected, y_resampled)

        joblib.dump(final_model, f"{MODEL_DIR}/model_{ticker}.pkl")
        joblib.dump(scaler, f"{MODEL_DIR}/scaler_{ticker}.pkl")
        joblib.dump(selector, f"{MODEL_DIR}/selector_{ticker}.pkl")

        print(f"  Model trained and saved for {ticker}")
    except Exception as exc:  # pragma: no cover - runtime issue
        print(f"  Failed training for {ticker}: {exc}")


def main() -> None:
    print(f"Starting upgraded training pipeline: {datetime.today().strftime('%Y-%m-%d')}")
    for ticker in TICKERS:
        train_model_for_ticker(ticker)


if __name__ == "__main__":  # pragma: no cover
    main()
