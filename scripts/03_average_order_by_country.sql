-- 3. Average order value by country
WITH orders AS(
	SELECT 
		t.invoice_no AS order,
		SUM(t.total_amount::numeric) AS total_value
	FROM transactions t
	GROUP BY t.invoice_no
),
total_sellings AS(
	SELECT 
		SUM(t.total_amount::numeric) AS total_sellings,
		AVG(t.total_amount::numeric) AS avg_order_total
	FROM transactions t
)
SELECT 
	co.country_name AS country,	
	ROUND(AVG(o.total_value), 2) AS avg_order,
	ROUND(SUM(o.total_value), 2) AS total_revenue,
	ROUND((SUM(o.total_value) / ts.total_sellings) * 100, 2) AS pct_revenue
FROM orders o
JOIN invoices i ON o.order = i.invoice_no
CROSS JOIN total_sellings ts
JOIN customers cu ON i.customer_id = cu.customer_id
JOIN countries co ON cu.country_id = co.country_id
GROUP BY co.country_name, ts.total_sellings
ORDER BY pct_revenue DESC;

	