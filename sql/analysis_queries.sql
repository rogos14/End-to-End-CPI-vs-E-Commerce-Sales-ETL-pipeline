-- ORDERS MADE EACH MONTH
SELECT 
	dd.year,
	dd.month, 
	SUM(ffs.total_orders) AS monthly_orders
FROM fact_sales ffs
JOIN dim_date dd
	ON ffs.date_id = dd.date_id
GROUP BY dd.year, dd.month
ORDER BY dd.year, dd.month;

-- Months with highest CPI
SELECT 
	dd.year,
	dd.month, 
	fc.value
FROM fact_cpi fc
JOIN dim_date dd
	ON fc.date_id = dd.date_id
ORDER BY fc.value DESC LIMIT 5;

-- PRODUCT CATEGORY SOLD THE MOST DURING HIGH CPI months
SELECT 
	dd.year,
	dd.month,
	dp.category_name,
	fc.value,
	ROUND(SUM(fss.total_sales)::numeric, 2) AS total_revenue
FROM fact_sales fss

JOIN dim_date dd
	ON fss.date_id = dd.date_id

JOIN fact_cpi fc
	ON fss.date_id = fc.date_id

JOIN dim_product dp
	ON fss.product_id = dp.product_id

GROUP BY
	dd.year, 
	dd.month,
	dp.category_name,
	fc.value

ORDER BY 
	fc.value DESC,
	total_revenue DESC

-- Months with high CPI but low sales
SELECT
    dd.year,
    dd.month,
    fc.cpi_value,
    ROUND(SUM(fs.total_sales)::numeric, 2) AS total_revenue
FROM fact_sales fs

JOIN dim_date dd
    ON fs.date_id = dd.date_id

JOIN fact_cpi fc
    ON fs.date_id = fc.date_id

GROUP BY
    dd.year,
    dd.month,
    fc.cpi_value

HAVING
    fc.cpi_value > (
        SELECT AVG(cpi_value)
        FROM fact_cpi
    )
    AND
    SUM(fs.total_sales) < (
        SELECT AVG(monthly_sales)
        FROM (
            SELECT
                SUM(total_sales) AS monthly_sales
            FROM fact_sales
            GROUP BY date_id
        ) sales_subquery
    )

ORDER BY
    fc.cpi_value DESC,
    total_revenue ASC;

