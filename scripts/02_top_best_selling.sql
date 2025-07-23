-- 2. Top 15 best selling products
SELECT 
	t.stock_code,
	p.description,
	ROUND(SUM(t.total_amount)::numeric, 2) AS total_revenue
FROM transactions t
JOIN products p ON t.stock_code = p.stock_code
WHERE t.stock_code NOT IN ('DOT', 'POST')
GROUP BY t.stock_code, p.description
ORDER BY total_revenue DESC
LIMIT 15;