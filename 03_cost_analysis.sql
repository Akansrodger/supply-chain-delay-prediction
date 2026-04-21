-- Monthly Spend by Supplier
SELECT 
    strftime('%Y-%m', d.order_date) AS month,
    s.supplier_name,
    COUNT(d.delivery_id) AS num_deliveries,
    SUM(d.quantity_mt) AS total_quantity_mt,
    ROUND(AVG(d.unit_price_usd), 2) AS avg_price_per_mt,
    ROUND(SUM(d.total_value_usd), 2) AS total_spend
FROM deliveries d
JOIN suppliers s ON d.supplier_id = s.supplier_id
GROUP BY month, s.supplier_name
ORDER BY month DESC, total_spend DESC;