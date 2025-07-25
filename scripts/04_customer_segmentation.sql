-- 4. Customer segmentation by purchase behavior
SELECT 
	c.customer_id,
	c.customer_type,
	COUNT(DISTINCT t.invoice_no) AS total_purchases,
	CASE
		WHEN COUNT(DISTINCT t.invoice_no) >= 20 THEN 'Frequent buyer'
		WHEN COUNT(DISTINCT t.invoice_no) BETWEEN 5 AND 19 THEN 'Occasional Buyer'
		ELSE 'Rare Buyer'
	END AS purchase_segment
FROM transactions t
JOIN invoices i ON t.invoice_no = i.invoice_no
JOIN customers c ON i.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY total_purchases DESC;
	


--- 4.1 RFM analysis
WITH customer_rfm AS (
    SELECT
        c.customer_id,
        c.customer_type,
        MAX(i.invoice_date) AS last_purchase_date,
        COUNT(DISTINCT t.invoice_no) AS frequency,
        SUM(t.total_amount) AS monetary
    FROM
        transactions t
    JOIN invoices i ON t.invoice_no = i.invoice_no
	JOIN customers c ON i.customer_id = c.customer_id
    GROUP BY
        c.customer_id
),
latest_date AS (
    SELECT MAX(invoice_date) AS latest_invoice_date
    FROM invoices
)
SELECT
    r.customer_id,
    r.customer_type,
    l.latest_invoice_date - last_purchase_date AS recency_time,
    CASE
        WHEN DATE_PART('day', l.latest_invoice_date - r.last_purchase_date) <= 30 THEN 'Recent Buyer'
        WHEN DATE_PART('day', l.latest_invoice_date - r.last_purchase_date) <= 90 THEN 'Engaged Buyer'
        ELSE 'At-Risk'
    END AS recency_segment,
    r.frequency,
    CASE
        WHEN r.frequency >= 10 THEN 'Frequent Buyer'
        WHEN r.frequency >= 5 THEN 'Regular Buyer'
        ELSE 'Occasional Buyer'
    END AS frequency_segment,
    ROUND(r.monetary::numeric, 2) AS monetary,
    CASE
        WHEN r.monetary >= 1000 THEN 'High Value'
        WHEN r.monetary >= 500 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS monetary_segment
FROM
    customer_rfm r
CROSS JOIN 
	latest_date l
ORDER BY
    r.monetary DESC;



--- 4.2 Full RFM analysis considering dinamic thresholds (percentiles)
WITH customer_rfm_raw AS (
    SELECT
        c.customer_id,
        MAX(i.invoice_date) AS last_purchase_date,
        COUNT(DISTINCT t.invoice_no) AS frequency,
        SUM(t.total_amount)::numeric AS monetary
    FROM transactions t
    JOIN invoices i ON t.invoice_no = i.invoice_no
    JOIN customers c ON i.customer_id = c.customer_id
    WHERE c.customer_type != 'Guest'
    GROUP BY c.customer_id
),
latest_date AS (
    SELECT MAX(invoice_date) AS latest_invoice_date FROM invoices
),
customer_rfm AS (
    SELECT
        r.*,
        DATE_PART('day', l.latest_invoice_date - r.last_purchase_date) AS recency_days
    FROM customer_rfm_raw r
    CROSS JOIN latest_date l
),
rfm_scores AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS recency_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS frequency_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS monetary_score
    FROM customer_rfm
),
rfm_labeled AS (
    SELECT *,
        CASE
            WHEN (recency_score + frequency_score + monetary_score) >= 13 THEN '1. Champions'
            WHEN (recency_score + frequency_score + monetary_score) >= 10 THEN '2. Loyal Customers'
            WHEN (recency_score + frequency_score + monetary_score) >=8 THEN '3. Potential Loyalists'
            WHEN (recency_score + frequency_score + monetary_score) >= 6 THEN '4. At Risk'
            ELSE '5. Lost'
        END AS segment
    FROM rfm_scores
)
SELECT 
    segment,
    COUNT(*) AS total_customers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage_customers,
    ROUND(AVG(recency_days::numeric), 1) AS avg_recency_days,
    ROUND(AVG(frequency), 1) AS avg_frequency,
    ROUND(AVG(monetary), 2) AS avg_monetary
FROM rfm_labeled
GROUP BY segment
ORDER BY segment;

