# supply-chain-delay-prediction
 Predictive analytics solution for supply chain optimization using ML and SQL.     Forecasts delivery delays with 74% ROC-AUC to identify high-risk suppliers     and optimize procurement decisions.


# 📊 Supply Chain Delay Prediction - GZ Industries

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Predictive analytics solution to forecast delivery delays and optimize supplier performance for aluminum can manufacturing.**

---

## 🎯 Project Overview

GZ Industries, West Africa's leading aluminum beverage can manufacturer, faced supply chain transparency challenges that led to production delays and increased costs. This project develops a machine learning solution to:

- **Predict delivery delays** 3+ days in advance with 74% ROC-AUC
- **Identify high-risk suppliers** through performance scoring
- **Quantify cost savings** of $150K+ annually through proactive intervention

---

## 📈 Key Results

| Metric | Value |
|--------|-------|
| **Model Accuracy** | 70% |
| **ROC-AUC Score** | 0.74 |
| **Delay Detection Rate** | 60% |
| **Projected Annual Savings** | $150,000+ |
| **Data Points Analyzed** | 500+ deliveries |
| **Suppliers Evaluated** | 15 international suppliers |

---

## 🛠️ Tech Stack

**Languages & Libraries:**
- Python 3.9+ (pandas, numpy, scikit-learn, matplotlib, seaborn)
- SQL (SQLite)

**Machine Learning:**
- Logistic Regression (primary model)
- Random Forest Classifier
- Time-series feature engineering


**Data Processing:**
- Rolling historical features (no data leakage)
- Time-based train/test splitting
- Feature importance analysis

---
---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.9+
pip
virtualenv (recommended)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/supply-chain-delay-prediction.git
cd supply-chain-delay-prediction
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Generate synthetic data**
```bash
python generate_data.py
```

5. **Run analysis**
```bash
python analyze_data.py
```

---

## 🔍 Key Features

### 1. **No Data Leakage**
- Rolling historical features computed only from past orders
- Time-based train/test split (train on older data, test on recent)
- Features available at order placement time only

### 2. **Advanced Feature Engineering**
- Supplier historical on-time rate (rolling 60-day window)
- Distance × Order size interaction
- Seasonal patterns (Q4 peak season detection)
- Risk composite scoring

### 3. **Business-Focused Metrics**
- Cost-benefit analysis ($10K per missed delay vs $500 per false alarm)
- Supplier risk segmentation (Low/Medium/High)
- ROI calculation for predictive intervention

---

## 📊 Sample Visualizations

### Supplier Performance Ranking
![Supplier Performance](visualizations/supplier_performance.png)

### ROC Curve - Model Performance
![ROC Curve](visualizations/roc_curve.png)

### Feature Importance Analysis
![Feature Importance](visualizations/feature_importance.png)

---

## 💡 Business Impact

**Problem Identified:**
- 30% of deliveries delayed by 5+ days
- $1.5M annual cost from emergency responses
- Limited visibility into supplier reliability

**Solution Delivered:**
- Predict 60% of delays before they occur
- Reduce emergency costs by $150K/year
- Data-driven supplier selection framework

**Key Recommendations:**
1. Prioritize suppliers within 500km (distance = #1 delay predictor)
2. Implement penalty clauses for suppliers with <70% on-time rate
3. Increase inventory buffer by 15% at high-risk locations

---

## 🎓 Learning Outcomes

**Technical Skills Demonstrated:**
- Machine learning model development & evaluation
- Time-series data handling without leakage
- SQL data extraction & analysis
- Data visualization for non-technical stakeholders
- Production-ready code structure

**Business Skills Demonstrated:**
- Translating business problems into ML tasks
- ROI-driven model optimization
- Executive-level communication
- Supply chain domain understanding

---

## 📧 Contact

**Akanle Tolulope**
- Email: akanletolulope08@gmail.com
- LinkedIn: [Your LinkedIn URL]
- Portfolio: [Your Portfolio URL]

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Project uses synthetic data modeling real-world aluminum supply chain operations
- Developed as a portfolio demonstration of predictive analytics capabilities

---

**⭐ If you found this project helpful, please consider giving it a star!**
