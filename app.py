import os
from pathlib import Path

import joblib
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "ride_demand_model.pkl"
DATA_PATH = BASE_DIR / "cleaned_data.csv"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "ridepulse-development-key")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None

try:
    model_package = joblib.load(MODEL_PATH)
    model = model_package["model"]
    low_threshold = float(model_package.get("low_threshold", 1.0))
    high_threshold = float(model_package.get("high_threshold", 2.0))
except Exception as exc:
    model = None
    low_threshold = 1.0
    high_threshold = 2.0
    app.logger.error("Unable to load model: %s", exc)


def get_locations():
    """Return model-supported start locations in a stable order."""
    if model is None:
        return []
    try:
        categories = model.named_steps["preprocessor"].named_transformers_["location"].categories_[0]
        return sorted(str(value) for value in categories)
    except (KeyError, AttributeError, IndexError):
        return []


def load_trips():
    """Prefer PostgreSQL, but fall back to the bundled cleaned dataset for demos."""
    try:
        if engine is None:
            raise SQLAlchemyError("DATABASE_URL is not configured")
        with engine.connect() as connection:
            trips = pd.read_sql(text("SELECT * FROM trips"), connection)
        if not trips.empty:
            return trips, "PostgreSQL"
    except SQLAlchemyError as exc:
        app.logger.info("Database unavailable; using CSV fallback: %s", exc)

    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH), "Bundled CSV"

    return pd.DataFrame(), "Unavailable"


def dashboard_metrics(trips):
    if trips.empty:
        return {
            "total_rides": 0,
            "total_locations": 0,
            "avg_miles": 0,
            "avg_duration": 0,
            "peak_hour": "—",
            "peak_day": "—",
        }

    trips = trips.copy()
    start_col = "start" if "start" in trips.columns else "start_location"
    hour_col = "hour_of_day"

    peak_hour = "—"
    if hour_col in trips.columns:
        peak_hour_value = trips[hour_col].value_counts().idxmax()
        peak_hour = f"{int(peak_hour_value):02d}:00"

    peak_day = "—"
    if "day_of_week_name" in trips.columns:
        peak_day = str(trips["day_of_week_name"].value_counts().idxmax())

    return {
        "total_rides": int(len(trips)),
        "total_locations": int(trips[start_col].nunique()),
        "avg_miles": round(float(trips["miles"].mean()), 2) if "miles" in trips else 0,
        "avg_duration": round(float(trips["duration_minutes"].mean()), 2) if "duration_minutes" in trips else 0,
        "peak_hour": peak_hour,
        "peak_day": peak_day,
    }


def chart_data(trips):
    if trips.empty:
        return {"hours": [], "ride_counts": [], "days": [], "day_counts": [], "locations": [], "location_counts": [], "categories": [], "category_counts": []}

    start_col = "start" if "start" in trips.columns else "start_location"

    hourly = trips.groupby("hour_of_day").size().reindex(range(24), fill_value=0)
    daily = (
        trips.groupby(["day_of_week", "day_of_week_name"])
        .size()
        .reset_index(name="ride_count")
        .sort_values("day_of_week")
    )
    locations = trips.groupby(start_col).size().sort_values(ascending=False).head(10)
    categories = trips.groupby("category").size().sort_values(ascending=False) if "category" in trips else pd.Series(dtype=int)

    return {
        "hours": [f"{hour:02d}:00" for hour in hourly.index],
        "ride_counts": hourly.astype(int).tolist(),
        "days": daily["day_of_week_name"].astype(str).tolist(),
        "day_counts": daily["ride_count"].astype(int).tolist(),
        "locations": locations.index.astype(str).tolist(),
        "location_counts": locations.astype(int).tolist(),
        "categories": categories.index.astype(str).tolist(),
        "category_counts": categories.astype(int).tolist(),
    }


@app.route("/")
def home():
    return render_template("index.html", locations=get_locations())


@app.post("/predict")
def predict():
    if model is None:
        flash("The prediction model could not be loaded. Check ride_demand_model.pkl.", "error")
        return redirect(url_for("home"))

    start = request.form.get("start", "").strip()
    time_value = request.form.get("time", "").strip()
    day_of_week_raw = request.form.get("day_of_week", "").strip()

    if not start or not time_value or not day_of_week_raw:
        flash("Please complete the location, time, and day fields.", "error")
        return redirect(url_for("home"))

    try:
        hour = int(time_value.split(":")[0])
        day_of_week = int(day_of_week_raw)
        if hour not in range(24) or day_of_week not in range(7):
            raise ValueError
    except (ValueError, TypeError):
        flash("Please provide a valid time and a day between Monday and Sunday.", "error")
        return redirect(url_for("home"))

    input_data = pd.DataFrame(
        {"start": [start], "hour_of_day": [hour], "day_of_week": [day_of_week]}
    )

    try:
        raw_prediction = max(0.0, float(model.predict(input_data)[0]))
    except Exception as exc:
        app.logger.exception("Prediction failed: %s", exc)
        flash("Prediction could not be completed for this selection.", "error")
        return redirect(url_for("home"))

    if raw_prediction <= low_threshold:
        status = "LOW"
        tone = "low"
        interpretation = "Historically quieter demand for this location and time combination."
    elif raw_prediction <= high_threshold:
        status = "MEDIUM"
        tone = "medium"
        interpretation = "Moderate historical demand for this location and time combination."
    else:
        status = "HIGH"
        tone = "high"
        interpretation = "Historically higher demand for this location and time combination."

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    return render_template(
        "result.html",
        status=status,
        tone=tone,
        raw_prediction=round(raw_prediction, 2),
        start=start,
        time=time_value,
        day=days[day_of_week],
        interpretation=interpretation,
    )


@app.get("/dashboard")
def dashboard():
    trips, source = load_trips()
    metrics = dashboard_metrics(trips)
    charts = chart_data(trips)
    return render_template("dashboard.html", metrics=metrics, charts=charts, data_source=source)


@app.get("/health")
def health():
    return {
        "service": "RidePulse",
        "status": "healthy" if model is not None else "degraded",
        "model_loaded": model is not None,
    }


@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", code=404, title="Page not found", message="The page you requested does not exist."), 404


@app.errorhandler(500)
def server_error(_error):
    return render_template("error.html", code=500, title="Something went wrong", message="RidePulse could not complete that request."), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
