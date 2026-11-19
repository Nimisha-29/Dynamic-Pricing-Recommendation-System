# Dynamic Pricing Recommendation System

## 1. Project Overview

The Dynamic Pricing Recommendation System is a Machine Learning-based application designed to help small businesses make better pricing decisions.

It analyzes product information, sales, demand, inventory levels and competitor pricing to recommend suitable selling prices instead of relying on fixed or manual pricing methods.

## 2. Objectives

- Recommend suitable product selling prices.
- Predict base prices using Machine Learning.
- Consider inventory levels and customer demand.
- Incorporate competitor pricing information.
- Maintain a minimum profit margin.
- Provide understandable explanations for price recommendations.

## 3. Technologies Used

- **Programming Language:** Python
- **Machine Learning:** Scikit-learn
- **Algorithm:** Random Forest Regression
- **Data Processing:** Pandas, NumPy
- **Explainable AI:** SHAP
- **Dashboard:** Streamlit
- **Visualization:** Plotly, Matplotlib
- **Model Storage:** Joblib

## 4. Key Features

- Product-based price recommendations.
- Random Forest-based base price prediction.
- Rule-based pricing adjustments.
- Inventory and demand analysis.
- Competitor price consideration.
- Minimum profit margin protection.
- SHAP-based model explainability.
- Interactive Streamlit dashboard.

## 5. Project Structure

```text
Dynamic-Pricing-Recommendation-System/
├── backend/
├── frontend/
├── data/
├── models/
├── notebooks/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 6. Dataset

The dataset contains product-level information such as:

- Date
- Product Name
- Cost Price
- Current Price
- Opening Stock
- Units Sold
- Closing Stock
- Demand Level

## 7. Installation and Setup

Clone the repository:

```bash
git clone https://github.com/Nimisha-29/Dynamic-Pricing-Recommendation-System.git
```

Navigate to the project directory:

```bash
cd Dynamic-Pricing-Recommendation-System
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## 8. Machine Learning Approach

The system uses Random Forest Regression to predict a suitable base price.

Rule-based adjustments then consider inventory, demand and competitor pricing while maintaining minimum profit margin constraints.

SHAP is used to explain the factors influencing the model's predictions.

## 9. Future Enhancements

- Real-time competitor price collection.
- Integration with business billing systems.
- Automated inventory updates.
- Continuous model retraining.
- Support for additional business categories.

## 10. Author

Developed as a Machine Learning project.
