WITH customer_age AS (
	SELECT 
		aggregate_id, 
		date_diff('year', date(date_parse(customer_dob, '%Y-%m-%d')), current_date) AS customer_age 
	FROM "events_db"."events" 
	WHERE customer_dob <> ''
),
accepted_orders AS (
	SELECT 
		COUNT(type) AS total_type_accepted, 
		customer_age 
	FROM "events_db"."events" e 
	JOIN customer_age ca ON e.aggregate_id=ca.aggregate_id 
	WHERE type='order_accepted' 
	GROUP BY customer_age
),
closed_orders AS (
	SELECT 
		e.aggregate_id, 
		type AS type_closed, 
		customer_age 
	FROM "events_db"."events" e 
	JOIN customer_age ca ON e.aggregate_id=ca.aggregate_id 
	WHERE type IN ('order_cancelled', 'order_fulfilled')
),
cancelled_orders AS (
	SELECT 
		count(type_closed) AS cancelled, 
		customer_age 
	FROM closed_orders 
	WHERE type_closed='order_cancelled' 
	GROUP BY customer_age)
SELECT 
	CAST(cancelled_orders.cancelled AS DOUBLE)/CAST(accepted_orders.total_type_accepted AS DOUBLE)*100 AS probability_to_cancel_order,
	cancelled_orders.customer_age 
FROM cancelled_orders 
JOIN accepted_orders ON cancelled_orders.customer_age=accepted_orders.customer_age 