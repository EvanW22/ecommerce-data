SELECT
    customer_id,
    first_name,
    last_name,
    email,
    city,
    state,
    created_at
FROM {{ source('ecommerce', 'customers') }}