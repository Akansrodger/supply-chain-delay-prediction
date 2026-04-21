-- Low Inventory Alerts (Below Reorder Point)
SELECT 
    date,
    location,
    aluminum_stock_mt,
    reorder_point_mt,
    days_of_supply,
    ROUND((reorder_point_mt - aluminum_stock_mt), 2) AS shortage_mt,
    CASE 
        WHEN days_of_supply < 7 THEN 'CRITICAL'
        WHEN days_of_supply < 14 THEN 'WARNING'
        ELSE 'OK'
    END AS alert_level
FROM inventory
WHERE aluminum_stock_mt < reorder_point_mt
ORDER BY days_of_supply ASC;