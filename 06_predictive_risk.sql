-- Suppliers at Risk of Future Delays (Last 90 Days Trend)
SELECT 
    s.supplier_name,
    s.supplier_tier,
    COUNT(d.delivery_id) AS recent_deliveries,
    ROUND(AVG(d.delay_days), 2) AS avg_delay_days,
    ROUND(SUM(CASE WHEN d.on_time = 'No' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS late_delivery_rate,
    sp.risk_level AS current_risk,
    CASE 
        WHEN AVG(d.delay_days) > 5 THEN 'High Risk'
        WHEN AVG(d.delay_days) > 2 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS predicted_risk
FROM deliveries d
JOIN suppliers s ON d.supplier_id = s.supplier_id
JOIN supplier_performance sp ON s.supplier_id = sp.supplier_id
WHERE d.order_date >= date('now', '-90 days')
GROUP BY s.supplier_name, s.supplier_tier, sp.risk_level
HAVING recent_deliveries >= 5
ORDER BY avg_delay_days DESC;