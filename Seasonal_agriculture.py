import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['axes.titleweight'] = 'bold'

pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 150)


# ---------------- Load & Explore ----------------
df = pd.read_excel("seasonal_agriculture_performance_dataset.xlsx")
print("Shape:", df.shape)
df.head()


df.info()


df.describe(include='all').T


for col in ['State', 'District', 'Crop', 'Season', 'Irrigation_Method']:
    print(f"{col} ({df[col].nunique()} unique): {sorted(df[col].unique())}")
    print()


missing = df.isnull().sum()
missing = missing[missing > 0]
print("Missing values per column:")
print(missing)
print("\nDuplicate rows:", df.duplicated().sum())


# ---------------- Cleaning ----------------
# Impute missing values using Season+Crop group median
for col in ['Rainfall_mm', 'Soil_Moisture_pct', 'Yield_Tonnes_Ha']:
    df[col] = df.groupby(['Season', 'Crop'])[col].transform(lambda x: x.fillna(x.median()))

# Fallback: any remaining NaNs (rare, small groups) filled with overall median
for col in ['Rainfall_mm', 'Soil_Moisture_pct', 'Yield_Tonnes_Ha']:
    df[col] = df[col].fillna(df[col].median())

print("Remaining missing values:", df.isnull().sum().sum())


# Outlier inspection using IQR method on Yield_Tonnes_Ha
Q1, Q3 = df['Yield_Tonnes_Ha'].quantile([0.25, 0.75])
IQR = Q3 - Q1
lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
outliers = df[(df['Yield_Tonnes_Ha'] < lower) | (df['Yield_Tonnes_Ha'] > upper)]
print(f"Yield IQR bounds: [{lower:.2f}, {upper:.2f}]  |  Outlier rows: {len(outliers)} ({len(outliers)/len(df)*100:.1f}%)")
outliers[['Farm_ID','Season','Crop','Yield_Tonnes_Ha','Production_Tonnes','Farm_Area_Hectares']].sort_values('Yield_Tonnes_Ha', ascending=False).head(10)


# Cap extreme yield outliers at the 99th percentile per crop to avoid distorting season-level aggregates,
# while preserving genuine high performers below that threshold.
cap = df.groupby('Crop')['Yield_Tonnes_Ha'].transform(lambda x: x.quantile(0.99))
n_capped = (df['Yield_Tonnes_Ha'] > cap).sum()
df['Yield_Tonnes_Ha'] = np.minimum(df['Yield_Tonnes_Ha'], cap)
print(f"Capped {n_capped} extreme yield values at each crop's 99th percentile.")


# Derived economic metrics
df['Cost_per_Hectare'] = df['Total_Cost_INR'] / df['Farm_Area_Hectares']
df['Revenue_per_Hectare'] = df['Revenue_INR'] / df['Farm_Area_Hectares']
df['Profit_per_Hectare'] = df['Profit_INR'] / df['Farm_Area_Hectares']
df['Profit_Margin_pct'] = (df['Profit_INR'] / df['Revenue_INR']) * 100

df[['Cost_per_Hectare','Revenue_per_Hectare','Profit_per_Hectare','Profit_Margin_pct']].describe().T


# ---------------- Season distribution ----------------
season_counts = df['Season'].value_counts()
fig, ax = plt.subplots(1, 2, figsize=(12,4.5))
sns.countplot(data=df, x='Season', order=season_counts.index, ax=ax[0])
ax[0].set_title('Number of Farm Records per Season')
ax[0].set_ylabel('Count')

season_crop = pd.crosstab(df['Season'], df['Crop'])
season_crop.plot(kind='bar', stacked=True, ax=ax[1], colormap='tab20')
ax[1].set_title('Crop Composition within Each Season')
ax[1].legend(bbox_to_anchor=(1.02,1), loc='upper left', fontsize=8)
plt.tight_layout()
plt.show()


# ---------------- Environmental conditions by season ----------------
env_cols = ['Rainfall_mm','Avg_Temperature_C','Humidity_pct','Sunlight_Hours_Day','Soil_Moisture_pct']
season_env = df.groupby('Season')[env_cols].mean().round(2)
season_env


fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()
for i, col in enumerate(env_cols):
    sns.boxplot(data=df, x='Season', y=col, ax=axes[i])
    axes[i].set_title(col.replace('_',' '))
axes[-1].axis('off')
plt.suptitle('Distribution of Environmental Conditions by Season', fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()


# ---------------- Yield & production by season ----------------
perf_cols = ['Yield_Tonnes_Ha','Production_Tonnes','Water_Efficiency_t_per_1000m3','Disease_Pest_Risk_pct']
season_perf = df.groupby('Season')[perf_cols].agg(['mean','median','std']).round(2)
season_perf


fig, axes = plt.subplots(1, 2, figsize=(13,5))
sns.violinplot(data=df, x='Season', y='Yield_Tonnes_Ha', ax=axes[0], inner='quartile')
axes[0].set_title('Yield (Tonnes/Ha) Distribution by Season')

sns.barplot(data=df, x='Season', y='Water_Efficiency_t_per_1000m3', ax=axes[1], estimator=np.mean, errorbar='sd')
axes[1].set_title('Avg Water Efficiency by Season')
plt.tight_layout()
plt.show()


# ---------------- Economic performance by season ----------------
econ_cols = ['Cost_per_Hectare','Revenue_per_Hectare','Profit_per_Hectare','Profit_Margin_pct']
season_econ = df.groupby('Season')[econ_cols].mean().round(0)
season_econ


fig, axes = plt.subplots(1, 2, figsize=(13,5))
season_econ[['Cost_per_Hectare','Revenue_per_Hectare']].plot(kind='bar', ax=axes[0])
axes[0].set_title('Avg Cost vs Revenue per Hectare by Season')
axes[0].set_ylabel('INR')
axes[0].tick_params(axis='x', rotation=0)

sns.boxplot(data=df, x='Season', y='Profit_Margin_pct', ax=axes[1])
axes[1].set_title('Profit Margin % Distribution by Season')
plt.tight_layout()
plt.show()


# ---------------- Crop x Season heatmap ----------------
pivot_yield = df.pivot_table(index='Crop', columns='Season', values='Yield_Tonnes_Ha', aggfunc='mean')
pivot_profit = df.pivot_table(index='Crop', columns='Season', values='Profit_per_Hectare', aggfunc='mean')

fig, axes = plt.subplots(1, 2, figsize=(14,6))
sns.heatmap(pivot_yield, annot=True, fmt='.1f', cmap='YlGnBu', ax=axes[0])
axes[0].set_title('Avg Yield (t/ha) — Crop x Season')

sns.heatmap(pivot_profit, annot=True, fmt='.0f', cmap='YlOrRd', ax=axes[1])
axes[1].set_title('Avg Profit per Hectare (INR) — Crop x Season')
plt.tight_layout()
plt.show()


# ---------------- State-wise breakdown ----------------
state_season_profit = df.pivot_table(index='State', columns='Season', values='Profit_per_Hectare', aggfunc='mean')
state_season_profit.plot(kind='bar', figsize=(12,5))
plt.title('Avg Profit per Hectare by State and Season')
plt.ylabel('INR / Hectare')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()


# ---------------- Irrigation method effectiveness ----------------
irr_season = df.groupby(['Season','Irrigation_Method'])[['Yield_Tonnes_Ha','Water_Efficiency_t_per_1000m3']].mean().round(2)
irr_season


fig, ax = plt.subplots(figsize=(11,5))
sns.barplot(data=df, x='Season', y='Water_Efficiency_t_per_1000m3', hue='Irrigation_Method', ax=ax)
ax.set_title('Water Efficiency by Irrigation Method Across Seasons')
plt.tight_layout()
plt.show()


# ---------------- Correlation / relationships ----------------
corr_cols = ['Rainfall_mm','Avg_Temperature_C','Humidity_pct','Sunlight_Hours_Day','Soil_pH',
             'Soil_Moisture_pct','Nitrogen_kg_ha','Phosphorus_kg_ha','Potassium_kg_ha',
             'Fertilizer_kg_ha','Pesticide_Litre_ha','Seed_Quality_Score','Yield_Tonnes_Ha']

fig, axes = plt.subplots(1, 3, figsize=(16,5))
for ax, season in zip(axes, df['Season'].unique()):
    sub = df[df['Season']==season][corr_cols]
    corr = sub.corr()[['Yield_Tonnes_Ha']].drop('Yield_Tonnes_Ha').sort_values('Yield_Tonnes_Ha')
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, cbar=False)
    ax.set_title(f'{season}: Correlation with Yield')
plt.tight_layout()
plt.show()


# Scatter: Rainfall vs Yield, colored by season
fig, ax = plt.subplots(figsize=(9,5.5))
sns.scatterplot(data=df, x='Rainfall_mm', y='Yield_Tonnes_Ha', hue='Season', alpha=0.5, ax=ax)
sns.regplot(data=df, x='Rainfall_mm', y='Yield_Tonnes_Ha', scatter=False, color='black', ax=ax, line_kws={'linestyle':'--'})
ax.set_title('Rainfall vs Yield by Season')
plt.tight_layout()
plt.show()


# ---------------- Disease/Pest risk ----------------
fig, ax = plt.subplots(figsize=(9,5))
sns.boxplot(data=df, x='Season', y='Disease_Pest_Risk_pct', ax=ax)
ax.set_title('Disease/Pest Risk % Distribution by Season')
plt.tight_layout()
plt.show()

df.groupby('Season')['Disease_Pest_Risk_pct'].mean().round(1)


# ---------------- Statistical Testing (One-way ANOVA) ----------------
test_cols = ['Yield_Tonnes_Ha','Profit_per_Hectare','Water_Efficiency_t_per_1000m3','Disease_Pest_Risk_pct','Rainfall_mm']
results = []
for col in test_cols:
    groups = [g[col].values for _, g in df.groupby('Season')]
    f_stat, p_val = stats.f_oneway(*groups)
    results.append({'Metric': col, 'F-statistic': round(f_stat,2), 'p-value': f"{p_val:.4g}",
                     'Significant (p<0.05)': 'Yes' if p_val < 0.05 else 'No'})

anova_results = pd.DataFrame(results)
anova_results


# ---------------- Cost-Revenue-Profit Relationship ----------------
fig, ax = plt.subplots(figsize=(9,5.5))
sns.scatterplot(data=df, x='Cost_per_Hectare', y='Revenue_per_Hectare', hue='Season', alpha=0.5, ax=ax)
lims = [df['Cost_per_Hectare'].min(), df['Cost_per_Hectare'].max()]
ax.plot(lims, lims, 'k--', alpha=0.4, label='Break-even (Revenue = Cost)')
ax.legend()
ax.set_title('Cost vs Revenue per Hectare by Season (points above line = profitable)')
plt.tight_layout()
plt.show()

loss_pct = (df['Profit_INR'] < 0).groupby(df['Season']).mean() * 100
print("Share of loss-making farms by season (%):")
print(loss_pct.round(1))


# ---------------- Consolidated Seasonal Summary ----------------
summary = df.groupby('Season').agg(
    Avg_Rainfall_mm=('Rainfall_mm','mean'),
    Avg_Temperature_C=('Avg_Temperature_C','mean'),
    Avg_Yield_t_ha=('Yield_Tonnes_Ha','mean'),
    Avg_Water_Efficiency=('Water_Efficiency_t_per_1000m3','mean'),
    Avg_Disease_Risk_pct=('Disease_Pest_Risk_pct','mean'),
    Avg_Profit_per_Ha=('Profit_per_Hectare','mean'),
    Avg_Profit_Margin_pct=('Profit_Margin_pct','mean'),
    Pct_Loss_Making_Farms=('Profit_INR', lambda x: (x<0).mean()*100)
).round(2)
summary
