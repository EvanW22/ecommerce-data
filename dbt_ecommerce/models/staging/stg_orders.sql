SELECT
    order_id,
    customer_id,
    order_date,
    status
FROM {{ source('ecommerce', 'orders') }}