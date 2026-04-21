-- Suppliers with High Defect Rates
SELECT 
    s.supplier_name,
    s.country,
    COUNT(d.delivery_id) AS total_deliveries,
    ROUND(AVG(d.defect_rate) * 100, 2) AS avg_defect_rate_pct,
    SUM(CASE WHEN d.quality_grade = 'C' THEN 1 ELSE 0 END) AS grade_c_deliveries,
    ROUND(AVG(d.defect_rate) * SUM(d.quantity_mt), 2) AS estimated_defect_mt
FROM deliveries d
JOIN suppliers s ON d.supplier_id = s.supplier_id
GROUP BY s.supplier_name, s.country
HAVING avg_defect_rate_pct > 3
ORDER BY avg_defect_rate_pct DESC;