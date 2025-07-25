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


-- 1.1 Monthly revenue trends with % change
WITH orders AS (
    SELECT 
        t.invoice_no AS order,
        SUM(t.total_amount) AS total_value
    FROM transactions t
    GROUP BY t.invoice_no
),
monthly_revenue AS (
    SELECT 
        TO_CHAR(i.invoice_date, 'YYYY-MM') AS month_year,
        ROUND(SUM(o.total_value)::numeric, 2) AS total_revenue,
        ROUND(AVG(o.total_value)::numeric, 2) AS avg_order
    FROM orders o
    JOIN invoices i ON o.order = i.invoice_no
    GROUP BY month_year
)
SELECT 
    month_year,
    avg_order,
    total_revenue,
    ROUND(
        CASE 
            WHEN LAG(total_revenue) OVER (ORDER BY month_year) IS NULL THEN NULL
            ELSE ((total_revenue - LAG(total_revenue) OVER (ORDER BY month_year)) / LAG(total_revenue) OVER (ORDER BY month_year)) * 100
        END,
        2
    ) AS revenue_pct_change
FROM monthly_revenue
ORDER BY month_year;
