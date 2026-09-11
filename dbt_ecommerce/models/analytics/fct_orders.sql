SELECT
    o.order_id,
    o.customer_id,
    oi.product_id,
    o.order_date,
    o.status,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS order_item_revenue
FROM {{ ref('stg_orders') }} AS o
JOIN {{ ref('stg_order_items') }} AS oi
    ON o.order_id = oi.order_id