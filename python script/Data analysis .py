''' EDA & STATISTICAL ANALYSIS WITH KEY QUESTIONS '''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os

## Define the directory and the log file name
log_dir = r'D:\\pharmaceutical_inventory analysis and optimization project-1\log'
log_file = os.path.join(log_dir, 'pipeline.log')  # You can name the file anything

## Make sure the directory exists
os.makedirs(log_dir, exist_ok=True)

## Set up logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


df = pd.read_csv("D:\\pharmaceutical_inventory analysis and optimization project-1\\Dataset\\cleaned_pharma_inventory.csv")
df["date"] = pd.to_datetime(df["date"])

logging.info("initiate analyzing the data... ")

# Which product classes generate the most revenue
df.groupby("product_class")["sales"].sum().sort_values().plot(kind = "barh")
plt.title("sales by product_class")
plt.tight_layout()
plt.show()

# Which cities shows erratic or volatile demand
sns.boxplot (x = "city", y = "sales", data =df)
plt.xticks(rotation=45)
plt.title("sale varience by cities")
plt.tight_layout()
plt.show()

# What drives sales more ----price or quantity
sns.heatmap(df[["sales", "quantity", "price"]].corr(), annot=True)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()

logging.info("Post-EDA complete....")

# is there any statistically significant channel difference
from scipy.stats import ttest_ind
logging.info("INTIATING THE STATISTICAL ANALYSIS...")
## Filter sales data by channel
pharmacy = df[df["channel"] == "Pharmacy"]["sales"]
hospital = df[df["channel"] == "Hospital"]["sales"]

## Perform independent t-test
t_stat, p_val = ttest_ind(pharmacy, hospital, equal_var=False)  # Welch’s t-test is safer if variances differ

## Print test statistics
print(f"T-statistic: {t_stat:.3f}, P-value: {p_val:.3f}")

## Interpret result
alpha = 0.05
if p_val < alpha:
    print(" Statistically significant difference in sales between Pharmacy and Hospital channels.")
else:
    print("No statistically significant difference in sales between Pharmacy and Hospital channels.")
    
logging.info("ttest_ independent completed...")   

 
# What is the sales trend over the time for (knowing the seasonality;)
df.groupby("month")["sales"].sum().plot(marker = "o")
plt.title("Monthly sales Trend")
plt.ylabel("sales")
plt.grid(True)
plt.tight_layout()
plt.show()

logging.info("Analyzing the seasonality.....")

# Where is product expiry risk higher  (to highlight the risk zones;)
## Group data to assess expiry risk

logging.info("Checking for risk_matrix...")
risk_df = df.groupby(["city", "product_class"]).agg({
    "sales": ['count', 'std'],
    "quantity": 'sum'
}).reset_index()

## Rename flattened columns
risk_df.columns = ['city', 'product_class', 'sales_count', 'sales_std', 'quantity_sum']

## Define expiry risk conditions
risk_df['expiry_alert'] = risk_df.apply(
    lambda x: "HIGH RISK" if (x['sales_count'] < 3 and x['quantity_sum'] > 50) else "NORMAL",
    axis=1
)

## Save to CSV
risk_df.to_csv("report of expiry check", index=False)

logging.info("Task completed....")