# 🚕 RidePulse

### Historical Ride Demand Analytics & Prediction Platform

RidePulse is a full-stack **data analytics and machine learning application** that turns historical ride records into an interactive demand intelligence experience.

The project combines **Python, Pandas, Scikit-learn, Flask, PostgreSQL, SQLAlchemy and Chart.js** to demonstrate the complete journey from raw data to an accessible web application.

> **Important:** RidePulse estimates historical recorded demand. It is not a real-time driver availability or live dispatch system.

---

## ✨ What RidePulse Does

### 1. Historical demand prediction

A user selects:

- Starting location
- Time of day
- Day of week

The saved machine-learning pipeline estimates the number of historically recorded rides for that combination and classifies the result as **LOW, MEDIUM or HIGH** demand.

### 2. Interactive analytics dashboard

The dashboard presents:

- Total recorded rides
- Unique starting locations
- Average trip distance
- Average trip duration
- Peak recorded hour
- Most active day
- 24-hour demand pattern
- Demand by day of week
- Top starting locations
- Ride category mix

### 3. Resilient data layer

RidePulse prefers **PostgreSQL** for application analytics. If PostgreSQL is unavailable, the dashboard automatically falls back to the bundled `cleaned_data.csv` dataset, making the project easier to demonstrate locally.

---

## 🧠 Machine Learning Pipeline

The final saved model uses:

- `start` — categorical starting location
- `hour_of_day` — hour from 0–23
- `day_of_week` — Monday=0 through Sunday=6

The preprocessing and estimator are stored together in a Scikit-learn `Pipeline`:

```text
Starting location ──► OneHotEncoder ──┐
                                      ├──► Random Forest Regressor ──► Demand estimate
Hour of day ──────────────────────────┤
Day of week ──────────────────────────┘
```

The saved artifact is `ride_demand_model.pkl`.

### Model evaluation from the original training experiment

| Metric | Value |
|---|---:|
| MAE | 0.539 |
| RMSE | 1.052 |
| R² | 0.348 |

These metrics should be treated as the evaluation of the current MVP model, not as a guarantee of production forecasting performance.

---

## 📊 Data Workflow

```text
Raw_Dataset.csv
      │
      ▼
Data Cleaning
      │
      ├── duration_minutes
      ├── month
      ├── day_of_week
      ├── hour_of_day
      ├── is_peak_hr
      └── is_weekend
      │
      ▼
cleaned_data.csv
      │
      ├──────────────► PostgreSQL / trips
      │
      └──────────────► ML demand dataset
                              │
                              ▼
                       Random Forest
                              │
                              ▼
                     Flask prediction app
                              │
                     ┌────────┴────────┐
                     ▼                 ▼
                 Prediction        Dashboard
```

---

## 🏗️ Project Structure

```text
RidePulse/
├── app.py
├── ride_demand_model.pkl
├── Raw_Dataset.csv
├── cleaned_data.csv
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── database/
│   ├── load_data.py
│   └── queries.sql
│
├── notebooks/
│   ├── data_cleaning.ipynb
│   ├── eda.ipynb
│   └── model_train.ipynb
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   ├── dashboard.html
│   └── error.html
│
├── static/
│   └── style.css
│
└── images/
    └── project reference images
```

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd RidePulse
```

### 2. Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials. **Never commit `.env` to GitHub.**

### 5. Create the database

Create a PostgreSQL database named:

```text
ridepulse
```

Then load the cleaned dataset:

```bash
python database/load_data.py
```

### 6. Start RidePulse

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/health
```

---

## 🔐 Configuration

The application reads configuration from environment variables:

```env
SECRET_KEY=your-secret
FLASK_DEBUG=false
PORT=5000
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/ridepulse
```

Database credentials are intentionally **not hard-coded** into the application.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Data processing | Pandas, NumPy |
| Machine learning | Scikit-learn, Random Forest |
| Model persistence | Joblib |
| Backend | Flask |
| Database | PostgreSQL |
| Database access | SQLAlchemy |
| Frontend | HTML, CSS, Jinja2 |
| Visualization | Chart.js |
| Configuration | python-dotenv |

---

## ⚠️ Current Limitations

- The dataset is relatively small and historical.
- Demand is defined from recorded trips rather than live platform activity.
- The current model uses only location and temporal features.
- Sparse location-hour-day combinations can reduce prediction reliability.
- The model should be retrained and re-evaluated before being used for operational decisions.

---

## 🔮 Future Improvements

1. Add weather and event features.
2. Add historical rolling-demand features.
3. Compare Random Forest with Gradient Boosting/XGBoost-style models.
4. Add confidence intervals or prediction uncertainty.
5. Add model versioning and experiment tracking.
6. Add automated data refresh pipelines.
7. Add authentication and role-based analytics access.
8. Deploy the application with Docker and a production WSGI server.

---

## 👨‍💻 Project Focus

RidePulse demonstrates practical skills across:

**Data Cleaning → Exploratory Analysis → Feature Engineering → SQL → Machine Learning → Model Serialization → Flask API/Web App → Dashboard Visualization → Production-minded Configuration**

---

## 📄 License

This project is intended for educational and portfolio use.
