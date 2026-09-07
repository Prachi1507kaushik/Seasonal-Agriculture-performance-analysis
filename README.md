**Seasonal Agriculture Performance Analysis**

**VOIS AICTE Batch 1 (2026–2027) — Major Project**

A data analytics project analyzing seasonal variation in agricultural performance across Indian states, using a farm-level dataset covering environmental conditions, resource usage, yield, and economic outcomes across the Kharif, Rabi, and Zaid cropping seasons.

1. Problem Statement

Agricultural activities are influenced by seasonal variations in environmental conditions, farming practices, resource availability, and market conditions. Raw agricultural data does not, by itself, explain how performance changes across seasons or what patterns can be observed. This project analyzes the dataset to identify meaningful seasonal patterns, trends, relationships, and variations that can support evidence-based agricultural planning.

2. Project Description

This project performs an end-to-end data analytics workflow — exploration, cleaning, visualization, correlation analysis, and statistical testing — on a 4,000-record agricultural dataset spanning:

8 states, 10 districts, 8 crops, 3 seasons, 4 irrigation methods
Environmental variables (rainfall, temperature, humidity, sunlight, soil pH/moisture)
Input variables (fertilizer, pesticide, NPK levels, seed quality)
Outcome variables (yield, production, revenue, cost, profit, water efficiency, disease/pest risk)

The full analysis is documented in a single executable Jupyter Notebook.

3. End Users
Farmers and agricultural cooperatives
Agricultural policy makers and government departments
Agricultural extension officers and advisors
Agribusiness and agri-input companies
Financial institutions / crop insurers
Researchers and students
4. Technology Used
Category	Tools


Data handling	pandas, NumPy
Visualization	Matplotlib, Seaborn
Statistical analysis	SciPy (scipy.stats.f_oneway)
Data source	Excel (.xlsx)
5. Project Structure
├── README.md
├── seasonal_agriculture_performance_dataset.xlsx   # Input dataset
└── Seasonal_Agriculture_Performance_Analysis.ipynb # Main analysis notebook
6. Dataset Overview
Column	Description
Farm_ID	Unique farm identifier
State, District	Location
Crop, Season	Crop type and cropping season (Kharif/Rabi/Zaid)
Farm_Area_Hectares	Size of the farm
Rainfall_mm, Avg_Temperature_C, Humidity_pct, Sunlight_Hours_Day	Environmental conditions
Soil_pH, Soil_Moisture_pct	Soil characteristics
Nitrogen_kg_ha, Phosphorus_kg_ha, Potassium_kg_ha, Fertilizer_kg_ha	Nutrient inputs
Irrigation_Method, Pesticide_Litre_ha, Seed_Quality_Score	Farming practices
Yield_Tonnes_Ha, Production_Tonnes	Production outcomes
Market_Price_INR_Tonne, Total_Cost_INR, Revenue_INR, Profit_INR	Economic outcomes
Water_Used_m3, Water_Efficiency_t_per_1000m3	Water usage metrics
Disease_Pest_Risk_pct	Risk indicator
7. Setup & Installation

Requirements: Python 3.9+

bash
pip install pandas numpy matplotlib seaborn scipy openpyxl jupyter
8. How to Run
Place seasonal_agriculture_performance_dataset.xlsx in the same directory as the notebook.
Launch Jupyter:
bash
   jupyter notebook
Open Seasonal_Agriculture_Performance_Analysis.ipynb.
Run all cells (Kernel → Restart & Run All).
9. Analysis Workflow
Data Loading & Exploration — shape, dtypes, summary statistics, missing values, duplicates
Data Cleaning — season/crop-aware median imputation, IQR-based outlier detection, percentile capping, derived per-hectare metrics
Seasonal Distribution — record counts and crop composition per season
Environmental Analysis — rainfall, temperature, humidity, sunlight, soil moisture by season
Yield & Production Analysis — yield distribution, water efficiency, disease/pest risk by season
Economic Analysis — cost, revenue, profit per hectare, profit margins, loss-making farm share
Crop × Season and State × Season Breakdowns — heatmaps identifying best-performing combinations
Irrigation Method Effectiveness — water efficiency comparison across seasons
Correlation Analysis — relationship between environmental/input factors and yield, by season
Statistical Testing — one-way ANOVA to test significance of seasonal differences
Insights & Recommendations — data-driven conclusions
10. Key Results
Environmental patterns matched expected agro-climatic behavior (highest rainfall/humidity in Kharif, lowest temperature in Rabi, highest sunlight in Zaid), validating dataset realism.
Yield, water efficiency, and disease/pest risk varied measurably by season, partly driven by which crops are grown in each season.
Revenue and profitability did not always move together — profit margin, not just revenue, is a more reliable success metric per season.
Drip/sprinkler irrigation generally outperformed flood/rainfed methods on water efficiency, with the gap most pronounced in the driest season.
One-way ANOVA confirmed statistically significant seasonal differences (p < 0.05) for yield, profit per hectare, water efficiency, disease risk, and rainfall.
A measurable share of farms operated at a loss in specific season-crop combinations, pointing to targeted intervention opportunities.

(Exact figures are generated live in the notebook's output cells.)

11. Future Scope
Extend to multi-year data to separate seasonal effects from year-specific anomalies
Build predictive models (regression/ML) for yield and profit forecasting
Integrate real-time weather forecast APIs for season-ahead recommendations
Add granular regional/soil-type data for hyper-local insights
Integrate market price forecasting to optimize sale timing
Deploy as an interactive dashboard (Streamlit/Power BI) for non-technical users
Model climate change scenarios and their impact on seasonal performance
12. Author

[Prachi kaushik] VOIS AICTE Batch 1, 2026–2027
