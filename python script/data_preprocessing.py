''' DATA PREPROCESSING'''
import pandas as pd
from sqlalchemy import create_engine
import logging
import os


#Define the directory and the log file name
log_dir = r'D:\\pharmaceutical_inventory analysis and optimization project-1\log'
log_file = os.path.join(log_dir, 'pipeline.log')  # You can name the file anything

# Make sure the directory exists
os.makedirs(log_dir, exist_ok=True)

## Set up logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Starting data cleaning and preprocessing...")

# connect with database using sqlalchemy
engine = create_engine("postgresql+psycopg2://postgres:Pkv758095@localhost:5432/practice")

# Execute SQL and load into a DataFrame
df = pd.read_sql("SELECT * FROM pharma_inventory", con=engine)

# Clean columns
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df['city'] = df['city'].str.strip()
df['channel'] = df['channel'].str.strip()

# Format values
df[['sales', 'price', 'quantity']] = df[['sales', 'price', 'quantity']].apply(pd.to_numeric, errors='coerce')
df["date"] = pd.to_datetime(df["month"] + "-" + df["year"].astype(str), format="%B-%Y")

# Remove incomplete rows
df.dropna(subset=["sales", "price", "quantity"], inplace=True)

# Save cleaned data to a new csc file
df.to_csv("cleaned_pharma_inventory.csv", index=False)
logging.info("Data cleaned and saved.")
