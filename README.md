# 🚕 RidePulse

### Intelligent Ride Demand Analytics & Machine Learning Platform

<p align="center">
  <strong>Transforming historical ride data into actionable analytics and demand insights.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web%20App-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Scikit--learn-Machine%20Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/Pandas-Data%20Analytics-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Chart.js-Visualization-FF6384?style=for-the-badge&logo=chart.js&logoColor=white" alt="Chart.js">
</p>

---

## 📌 Overview

**RidePulse** is a full-stack **data analytics and machine learning platform** designed to analyze historical ride activity and estimate recorded ride demand based on location and temporal patterns.

The application brings together the complete analytics workflow:

```text
Raw Data
   ↓
Data Cleaning
   ↓
Exploratory Data Analysis
   ↓
Feature Engineering
   ↓
SQL / PostgreSQL Analytics
   ↓
Machine Learning
   ↓
Flask Application
   ↓
Interactive Dashboard
   ↓
Demand Prediction
```

Rather than presenting analysis as a static notebook, RidePulse turns the underlying data and ML workflow into an interactive web application.

> **Scope:** RidePulse estimates demand from historical recorded ride data. It is not a live ride-dispatch, driver-availability, or real-time transportation system.

---

# ✨ Key Features

## 📊 Interactive Analytics Dashboard

Explore historical ride activity through a centralized dashboard containing:

- Total recorded rides
- Unique starting locations
- Average trip distance
- Average trip duration
- Peak recorded hour
- Most active day
- Hourly demand patterns
- Demand by day of week
- Top starting locations
- Ride category distribution

The dashboard is designed to make exploratory analysis easier to understand without requiring direct interaction with the underlying database.

---

## 🤖 Machine Learning Demand Prediction

RidePulse provides an interactive prediction workflow.

Users provide:

- 📍 Starting location
- 🕐 Hour of day
- 📅 Day of week

The trained model estimates the number of historically recorded rides associated with that combination.

The result is also translated into a simple demand category:

```text
LOW
MEDIUM
HIGH
```

This makes the model output easier to interpret from a business perspective.

---

## 🧠 Machine Learning Pipeline

The saved model combines preprocessing and prediction into a single Scikit-learn pipeline.

### Input Features

| Feature | Description |
|---|---|
| `start` | Starting ride location |
| `hour_of_day` | Hour of the day, 0–23 |
| `day_of_week` | Day index, Monday=0 → Sunday=6 |

### Pipeline

```text
                ┌─────────────────────┐
Starting ──────►│                     │
Location        │                     │
                │   OneHotEncoder     │
Hour ──────────►│                     │
                │                     ├──────► Random Forest
Day ───────────►│                     │          Regressor
                └─────────────────────┘              │
                                                     ▼
                                             Demand Estimate
                                                     │
                                                     ▼
                                             LOW / MEDIUM / HIGH
```

The preprocessing and estimator are stored together in:

```text
ride_demand_model.pkl
```

This helps keep the prediction pipeline consistent between training and application inference.

---

# 📈 Model Performance

The current model was evaluated during the original training experiment.

| Metric | Result |
|---|---:|
| MAE | **0.539** |
| RMSE | **1.052** |
| R² | **0.348** |

### What these metrics mean

- **MAE — 0.539:** average absolute prediction error in the experiment.
- **RMSE — 1.052:** gives additional weight to larger prediction errors.
- **R² — 0.348:** the model explains a portion of the observed variation in the experimental dataset.

> These results represent the current MVP experiment and should not be interpreted as production forecasting performance.

---

# 🗄️ Data Architecture

RidePulse uses a resilient data-access strategy.

### Primary data source

```text
PostgreSQL
```

### Local demonstration fallback

```text
cleaned_data.csv
```

If PostgreSQL is unavailable, the dashboard can fall back to the bundled cleaned dataset, making local demonstrations easier.

```text
             ┌──────────────────┐
             │    RidePulse     │
             │    Web App       │
             └────────┬─────────┘
                      │
               Analytics Layer
                      │
              ┌───────┴────────┐
              │                │
              ▼                ▼
        PostgreSQL        CSV Fallback
              │                │
              └───────┬────────┘
                      ▼
               Analytics Data
```

---

# 🔄 Data Processing Workflow

The project transforms raw ride records into analysis-ready data.

```text
Raw_Dataset.csv
      │
      ▼
Data Cleaning
      │
      ├── Duration calculation
      ├── Date/time extraction
      ├── Month extraction
      ├── Day-of-week extraction
      ├── Hour extraction
      ├── Peak-hour flag
      └── Weekend flag
      │
      ▼
cleaned_data.csv
      │
      ├───────────────► PostgreSQL
      │
      ├───────────────► SQL Analytics
      │
      └───────────────► ML Dataset
                              │
                              ▼
                       Feature Engineering
                              │
                              ▼
                       Random Forest Model
                              │
                              ▼
                       ride_demand_model.pkl
                              │
                              ▼
                         Flask Application
```

---

# 🏗️ Project Architecture

```text
RidePulse/
│
├── app.py                         # Flask application
├── ride_demand_model.pkl          # Trained ML pipeline
├── Raw_Dataset.csv                # Original dataset
├── cleaned_data.csv               # Processed dataset
│
├── database/
│   ├── load_data.py               # PostgreSQL data loader
│   └── queries.sql                # Analytics queries
│
├── notebooks/
│   ├── data_cleaning.ipynb        # Data preparation
│   ├── eda.ipynb                  # Exploratory analysis
│   └── model_train.ipynb          # Model training
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   ├── dashboard.html
│   └── error.html
│
├── static/
│   └── style.css                  # Application styling
│
├── images/
│   └── project reference images
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| ML Algorithm | Random Forest Regressor |
| Model Persistence | Joblib |
| Backend | Flask |
| Database | PostgreSQL |
| ORM / DB Layer | SQLAlchemy |
| Frontend | HTML5, CSS3, Jinja2 |
| Visualization | Chart.js |
| Configuration | python-dotenv |
| Development | Jupyter Notebook, Git, GitHub |

---

# 🚀 Getting Started

## Prerequisites

Make sure you have:

- Python 3.10+
- PostgreSQL
- Git
- pip

---

## 1. Clone the repository

```bash
git clone https://github.com/sathvikkasanagpttu/RidePulse.git
cd RidePulse
```

---

## 2. Create a virtual environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create your environment file:

### macOS / Linux

```bash
cp .env.example .env
```

### Windows

```powershell
copy .env.example .env
```

Then configure the values in `.env`:

```env
SECRET_KEY=your-secret-key
FLASK_DEBUG=false
PORT=5000
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/ridepulse
```

> Never commit your `.env` file or database credentials to GitHub.

---

# 🐘 PostgreSQL Setup

Create the database:

```sql
CREATE DATABASE ridepulse;
```

Then load the cleaned dataset:

```bash
python database/load_data.py
```

Once the database is configured, RidePulse can use PostgreSQL for application analytics.

If PostgreSQL is unavailable, the application can use the bundled cleaned CSV for local dashboard demonstrations.

---

# ▶️ Run the Application

Start the Flask application:

```bash
python app.py
```

Open the application:

```text
http://127.0.0.1:5000
```

Health endpoint:

```text
http://127.0.0.1:5000/health
```

---

# 🔐 Security & Configuration

RidePulse uses environment-based configuration rather than embedding sensitive database credentials directly into application code.

Example:

```env
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/ridepulse
```

The following files should remain local:

```text
.env
```

The repository provides:

```text
.env.example
```

as a safe configuration template.

---

# 📊 Analytics Capabilities

RidePulse provides several analytical perspectives on historical ride activity.

### Time Analysis

```text
Hourly demand
       ↓
Peak activity
       ↓
Daily patterns
       ↓
Weekend vs weekday behavior
```

### Location Analysis

```text
Starting locations
       ↓
Ride volume
       ↓
Top active locations
       ↓
Location-level demand patterns
```

### Trip Analysis

```text
Trip distance
       +
Trip duration
       +
Ride category
       ↓
Historical ride profile
```

---

# 🧪 Machine Learning Workflow

The model development process follows a standard ML workflow:

```text
1. Collect Dataset
       ↓
2. Clean Data
       ↓
3. Explore Data
       ↓
4. Engineer Features
       ↓
5. Split Dataset
       ↓
6. Train Model
       ↓
7. Evaluate Model
       ↓
8. Serialize Pipeline
       ↓
9. Integrate with Flask
       ↓
10. Serve Predictions
```

This separation between experimentation and application inference makes the project easier to understand and maintain.

---

# ⚠️ Current Limitations

RidePulse is currently an **MVP / portfolio analytics application**, so there are several limitations:

- The dataset represents historical recorded rides.
- The model does not consume real-time ride activity.
- The current feature set is relatively small.
- External factors such as weather and events are not included.
- Sparse combinations of location, hour, and day may produce less reliable estimates.
- Model performance may change when applied to new datasets.
- Production deployment would require additional monitoring and security controls.

---

# 🔮 Future Roadmap

### Phase 1 — Advanced Features

- Weather integration
- Holiday/event features
- Historical rolling demand
- Additional geographic features

### Phase 2 — ML Improvements

- Gradient Boosting models
- XGBoost-style approaches
- Hyperparameter optimization
- Cross-validation
- Feature importance analysis
- Prediction uncertainty

### Phase 3 — Production Engineering

- Docker containerization
- Production WSGI server
- Automated data pipelines
- Model versioning
- Experiment tracking
- Automated model retraining

### Phase 4 — Platform Features

- User authentication
- Role-based dashboards
- Admin analytics
- Model monitoring
- Data-quality monitoring
- Scheduled reports

---

# 🎯 Skills Demonstrated

RidePulse demonstrates practical experience across the complete data-to-application lifecycle:

```text
Data Collection
      ↓
Data Cleaning
      ↓
Exploratory Data Analysis
      ↓
Feature Engineering
      ↓
SQL Analytics
      ↓
Machine Learning
      ↓
Model Serialization
      ↓
Backend Development
      ↓
Dashboard Development
      ↓
Application Configuration
```

### Core Skills

**Python • SQL • Pandas • NumPy • Scikit-learn • Machine Learning • PostgreSQL • Flask • SQLAlchemy • Chart.js • Data Visualization • Feature Engineering • Exploratory Data Analysis • Git • GitHub**

---

# 💼 Portfolio Value

RidePulse demonstrates how a machine-learning experiment can be transformed into an interactive application.

Instead of stopping at:

```text
Dataset → Notebook → Model
```

the project extends the workflow to:

```text
Dataset
   ↓
Analytics
   ↓
Machine Learning
   ↓
Model Pipeline
   ↓
Backend
   ↓
Database
   ↓
Dashboard
   ↓
Interactive Prediction
```

This makes RidePulse suitable as a portfolio project for roles involving:

- Data Analytics
- Business Intelligence
- Machine Learning
- Python Development
- SQL / Database Analytics
- Backend Development

---

# 📜 License

This project is intended for educational, portfolio, and demonstration purposes.

---

# 👨‍💻 Author

### Sathvik Kasanagottu

**Computer Science & Engineering | Data Analytics | Machine Learning | Python | SQL**

GitHub:  
https://github.com/sathvikkasanagpttu

---

<p align="center">
  <strong>🚕 RidePulse — From Historical Ride Data to Actionable Demand Insights.</strong>
</p>

<p align="center">
  Built with Python • Flask • PostgreSQL • Scikit-learn • Pandas • Chart.js
</p>
