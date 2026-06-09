# 🚀 AI-Driven Customer Behavior Analytics

An end-to-end Machine Learning project designed to analyze customer behavior, predict churn, segment customers, and generate personalized product recommendations. The application provides interactive dashboards and predictive analytics to help businesses make data-driven decisions.

---

## 📌 Project Overview

This project leverages Machine Learning techniques to understand customer behavior patterns and improve customer retention strategies.

### Key Features

* 📊 Customer Segmentation using clustering algorithms
* 🔮 Customer Churn Prediction
* 🎯 Personalized Product Recommendations
* 📈 Interactive Analytics Dashboard
* 🤖 Machine Learning Model Training Pipeline
* 💾 Model Persistence and Deployment Ready Architecture

---

## 🛠️ Tech Stack

### Programming Language

* Python 3.10+

### Machine Learning

* Scikit-Learn
* Pandas
* NumPy
* Matplotlib
* Seaborn

### Dashboard & Visualization

* Streamlit
* Plotly

### Database

* SQLite / CSV Dataset

### Model Storage

* Pickle (.pkl)

---

## 📂 Project Structure

```text
AI-Driven-Customer-Behavior-Analytics/
│
├── models/
│   ├── recommendation.py
│   ├── segmentation.py
│   └── train_models.py
│
├── pages/
│   ├── dashboard.py
│   ├── churn.py
│   ├── prediction.py
│   ├── recommendations.py
│   └── segmentation.py
│
├── saved_models/
│   ├── churn_model.pkl
│   ├── segmentation_model.pkl
│   └── recommendation_model.pkl
│
├── dataset/
│   └── customer_data.csv
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/AI-Driven-Customer-Behavior-Analytics.git

cd AI-Driven-Customer-Behavior-Analytics
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## 📊 Machine Learning Workflow

### 1. Data Collection

Customer transaction and behavioral data is collected from datasets.

### 2. Data Preprocessing

* Missing value handling
* Feature engineering
* Data scaling
* Encoding categorical variables

### 3. Customer Segmentation

Customers are grouped based on purchasing behavior using clustering algorithms.

### 4. Churn Prediction

Classification models predict whether a customer is likely to leave.

### 5. Recommendation System

Products are recommended based on customer preferences and purchase history.

### 6. Dashboard Analytics

Interactive visualizations provide business insights and customer trends.

---

## 🎯 Features

### Customer Segmentation

* Behavioral clustering
* Customer group analysis
* Marketing strategy support

  <img width="1471" height="813" alt="Screenshot 2026-06-09 143614" src="https://github.com/user-attachments/assets/03293fa7-7117-4fcf-b425-9d3f67b22e26" />


### Churn Prediction

* Early churn detection
* Retention strategy insights
* Probability-based predictions
  <img width="1532" height="863" alt="Screenshot 2026-06-09 142905" src="https://github.com/user-attachments/assets/2fe7e30b-f62d-47c6-ac64-ebe0e7db206b" />


### Recommendation Engine

* Personalized recommendations
* Product affinity analysis
* Customer engagement improvement
  <img width="1900" height="867" alt="Screenshot 2026-06-09 142918" src="https://github.com/user-attachments/assets/fd28c3c7-8bb1-4202-8f93-e173a9e3cf89" />


### Dashboard

* KPI Monitoring
* Customer Insights
* Sales Analysis
* Visual Reports

<img width="1882" height="856" alt="Screenshot 2026-06-09 142840" src="https://github.com/user-attachments/assets/12aabd47-2f9b-48b5-b687-8a7c0f17d5f5" />


## 📈 Future Enhancements

* Deep Learning Models
* Real-Time Customer Analytics
* Cloud Deployment
* API Integration
* Advanced Recommendation Algorithms
* Customer Lifetime Value Prediction

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Developed as a Machine Learning project for Customer Behavior Analytics and Business Intelligence.

⭐ If you found this project useful, consider giving it a star on GitHub.
