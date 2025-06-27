-- 1. Create Table Schema
CREATE TABLE pharma_inventory (
  distributor VARCHAR,
  customer_name VARCHAR,
  city VARCHAR,
  country VARCHAR,
  latitude FLOAT,
  longitude FLOAT,
  channel VARCHAR,
  sub_channel VARCHAR,
  product_name VARCHAR,
  product_class VARCHAR,
  quantity INT,
  price NUMERIC,
  sales NUMERIC,
  month VARCHAR,
  year INT,
  name_of_sales_rep VARCHAR,
  manager VARCHAR,
  sales_team VARCHAR
);

--2. Load the data 
COPY pharma_inventory FROM 'D:\\pharmaceutical_inventory analysis and optimization project-1\\Dataset\\uncleaned_pharma_inventory.csv'
DELIMITER ',' CSV HEADER;

-- 3. Validate Record Count & Missing Values
SELECT * FROM pharma_inventory;
SELECT COUNT(*) FROM pharma_inventory;
SELECT COUNT(*) FROM pharma_inventory WHERE sales IS NULL OR quantity IS NULL;

-- 4. Preview Sales by Product Class
SELECT product_class, SUM(sales) FROM pharma_inventory GROUP BY product_class ORDER BY 2 DESC;
SELECT product_class, 
       ROUND(SUM(sales), 2) AS total_sales
FROM  pharma_inventory
GROUP BY product_class
ORDER BY total_sales DESC;

-- 5. Compare Channels
SELECT channel, 
       ROUND(AVG(sales),2) FROM pharma_inventory GROUP BY channel;