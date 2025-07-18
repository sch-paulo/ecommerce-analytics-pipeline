-- 1. Monthly revenue trends
WITH orders AS(
	SELECT 
		t.invoice_no AS order,
		SUM(t.total_amount) AS total_value
	FROM transactions t
	GROUP BY t.invoice_no
)
SELECT 
	TO_CHAR(i.invoice_date, 'YYYY-MM') AS month_year,
	ROUND(SUM(o.total_value)::numeric, 2) AS total_revenue,
	ROUND(AVG(o.total_value)::numeric, 2) AS avg_order
FROM orders o
JOIN invoices i ON o.order = i.invoice_no
GROUP BY month_year
ORDER BY month_year;