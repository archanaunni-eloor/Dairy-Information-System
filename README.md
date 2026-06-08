# 🥛 ML-Driven Dairy Procurement Optimization & Analytics Engine

An end-to-end Data Science and Machine Learning web application built using **Python, Streamlit, Scikit-learn, and SQLite**. This platform is designed to modernize cooperative dairy administration by transforming legacy procurement data into actionable operational insights and predictive production logic.

---

## 🚀 Key Features

### 1. Automated Data Ingestion Pipeline
* **Multi-format Support:** Seamlessly parses and uploads Excel/CSV procurement datasets.
* **Smart Schema Mapping:** Features a flexible data-cleaning layer that handles case-sensitivity, column renaming, and data-type normalization dynamically.
* **Robust Storage:** Implemented an transactional local database infrastructure using **SQLite** (`INSERT OR REPLACE` logs) to prevent data duplication.

### 2. Interactive Executive Dashboard
* **Operational KPIs:** Real-time calculation of key metrics including Total Milk Collected (supporting 432K+ Liters), Active Cattle Count, Average Farmer Age, and District-level AI (Artificial Insemination) metrics.
* **Advanced Data Visualizations:** Dynamic Plotly visualizations plotting procurement trends by society, seasonal volume fluctuations, and an **Inversely Proportional Study** correlating AI attempts against overall milk yield.

### 3. Machine Learning Predictive Engine
* **Yield Forecasting:** Utilizes a Scikit-learn `LinearRegression` model to forecast future production volumes based on interactive parameters.
* **Polynomial Feature Engineering:** Models the socio-economic law of diminishing returns by integrating quadratic features (`feed_squared`) for cattle feed inputs.
* **Proportional Scaling Logic:** Features custom multi-society simulation tracking baseline cattle and feed ratios to eliminate average-prediction biases.

### 4. Precision Feed Rationing Optimizer
* **Rule-based Logic:** Calculates daily dairy rations down to individual cow requirements.
* **Nutritional Breakdown:** Separates exact Maintenance Rations (fixed) and Production Rations (scaled precisely to daily lactation metrics) to optimize cost-to-yield efficiency.

---

## 🛠️ Tech Stack & Libraries

* **Frontend/UI:** Streamlit (UI/UX design optimized with responsive structural components)
* **Data Processing:** Pandas, NumPy
* **Database Engine:** SQLite3
* **Machine Learning:** Scikit-learn (Linear Regression)
* **Data Visualization:** Plotly Express

---

## 📂 Project Architecture

```text
├── app.py                  # Main Streamlit Application (Multi-page configuration)
├── data.sqlite             # Local relational database storing procurement logs
├── requirements.txt        # Python dependency specifications
└── README.md               # Documentation

Installation & Setup

1. Clone the Repository

git clone [https://github.com/archanaunni-eloor/dairy-information-system.git](https://github.com/archanaunni-eloor/dairy-information-system.git)
cd dairy-information-system

2. Install Dependencies
Make sure you have Python 3.10+ installed. Install the required libraries using:
pip install -r requirements.txt

3. Run the Streamlit Application
streamlit run app.py

Application Preview & Data Template
The system expects data containing the following operational headers (either uppercase/lowercase or underscored formats are automatically validated):

Society_Name (e.g., Mannam KUCS, Vadakkumppuram)

Month (Procurement period)

Liters (Total milk collected)

Cattle_Count (Total active dairy cattle)

Feed_Qty_Kg (Concentrate feed distributed)

Avg_AI_Attempts & Avg_Farmer_Age

Shed_Score & Vaccination

💡 Industry Context
This system bridges the gap between field-level cooperative dairy metrics and strategic administration.
By leveraging predictive analytics, administrative authorities can simulate changing input costs (like feed volume) and preemptively balance supply chains based on reliable localized machine learning forecasts.
