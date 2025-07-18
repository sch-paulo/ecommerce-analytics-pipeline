-- 4. Average order value by country
WITH orders AS(
	SELECT 
		t.invoice_no AS order,
		SUM(t.total_amount) AS total_value
	FROM transactions t
	GROUP BY t.invoice_no
)
SELECT 
	co.country_name AS country,	
	ROUND(AVG(o.total_value)::numeric, 2) AS avg_order,
	ROUND(SUM(o.total_value)::numeric, 2) AS total_revenue
FROM orders o
JOIN invoices i ON o.order = i.invoice_no
JOIN customers cu ON i.customer_id = cu.customer_id
JOIN countries co ON cu.country_id = co.country_id
GROUP BY co.country_name
ORDER BY avg_order DESC;

	