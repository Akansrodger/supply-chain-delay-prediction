-- Deliveries with Delays > 5 Days
SELECT 
    d.delivery_id,
    s.supplier_name,
    d.order_date,
    d.expected_delivery_date,
    d.actual_delivery_date,
    d.delay_days,
    d.quantity_mt,
    d.total_value_usd,
    d.destination
FROM deliveries d
JOIN suppliers s ON d.supplier_id = s.supplier_id
WHERE d.delay_days > 5
ORDER BY d.delay_days DESC;