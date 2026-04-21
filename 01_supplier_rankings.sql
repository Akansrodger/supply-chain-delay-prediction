-- Top 10 Suppliers by Performance Score
SELECT 
    s.supplier_name,
    s.country,
    s.supplier_tier,
    sp.total_deliveries,
    ROUND(sp."on_time_rate_%", 2) AS on_time_rate,
    ROUND(sp."grade_a_rate_%", 2) AS quality_rate,
    ROUND(sp.performance_score, 2) AS overall_score,
    sp.risk_level
FROM supplier_performance sp
JOIN suppliers s ON sp.supplier_id = s.supplier_id
ORDER BY sp.performance_score DESC
LIMIT 10;