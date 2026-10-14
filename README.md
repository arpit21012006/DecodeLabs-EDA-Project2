# Exploratory Data Analysis (EDA) | DecodeLabs Internship

A Python-based **Exploratory Data Analysis project** developed as part of the DecodeLabs Data Analytics Internship.

This project analyzes an e-commerce transaction dataset to identify sales trends, product performance, statistical patterns, and potential outliers.

## Project Overview

The dataset contains **1,200 records and 14 columns**, including order details, product information, pricing, payment methods, and order statuses.

The analysis focuses on understanding data distributions, identifying anomalies, and extracting meaningful business insights.

## Key Features

- **Data Exploration:** Dataset structure, data types, missing values, and duplicate records.
- **Descriptive Statistics:** Mean, median, minimum, maximum, standard deviation, and frequency counts.
- **Outlier Detection:** Interquartile Range (IQR) method.
- **Trend Analysis:** Monthly sales, product revenue, payment methods, and order statuses.
- **Data Visualization:** Six charts using Matplotlib and Seaborn.
- **Automated Reporting:** Excel analysis reports and a final PDF report.

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- OpenPyXL
- SciPy
- ReportLab

## Project Structure

```text
DecodeLabs_EDA_Project2/
├── src/
│   ├── load_data.py
│   ├── descriptive_stats.py
│   ├── outlier_analysis.py
│   ├── trend_analysis.py
│   ├── visualize.py
│   └── generate_report.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Exploratory Data Analysis Results

| Metric | Result |
|---|---|
| Total Records | 1,200 |
| Total Features | 14 |
| Missing Values | 309 |
| Duplicate Rows | 0 |
| Average Order Value | 1,053.97 |
| Median Order Value | 823.62 |
| Potential Outliers | 8 |

**Key observations:** Missing values are concentrated in the `CouponCode` column. The IQR method identified eight potential outliers in `TotalPrice`, representing approximately 0.67% of the records.

## Generated Visualizations

The project produces six charts:

1. Monthly Sales Trend
2. Top 10 Products by Revenue
3. Payment Method Distribution
4. Order Status Distribution
5. Order Value Distribution
6. Numerical Feature Correlation Heatmap

## Installation and Usage

**1. Clone the repository**

```bash
git clone https://github.com/arpit21012006/DecodeLabs-EDA-Project2.git
cd DecodeLabs-EDA-Project2
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Prepare the dataset**

Create a `data` folder and place the authorized Excel dataset inside it, named:

`Dataset for Data Analytics.xlsx`

The dataset is not included in this public repository.

**4. Run the project**

```bash
python main.py
```

The pipeline generates statistical reports, trend analysis, outlier analysis, visualizations, and a PDF report.

## Privacy and Data Handling

The raw dataset and generated analysis files are excluded from the public repository using `.gitignore`.

## Conclusion

This project demonstrates practical skills in exploratory data analysis, statistical analysis, data visualization, and automated reporting using Python.

---

**Developer:** Arpit Sharma  
**Internship:** DecodeLabs  
**Project:** Exploratory Data Analysis (Project 2)
