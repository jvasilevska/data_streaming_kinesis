WITH accepted_orders AS (
	SELECT 
		id AS accepted_order_id, 
		aggregate_id, 
		type, 
		date_parse(SUBSTR(timestamp,1,19), '%Y-%m-%d %H:%i:%s') AS accepted_order_timestamp 
	FROM "events_db"."events" 
	WHERE type='order_accepted'
),
fulfilled_orders AS (
	SELECT 
		id AS closed_orders_id, 
		aggregate_id, 
		type, 
		date_parse(SUBSTR(timestamp,1,19),'%Y-%m-%d %H:%i:%s') AS fulfilled_orders_timestamp 
	FROM "events_db"."events" 
	WHERE type='order_fulfilled'
),
processing_time AS (
	SELECT
		ao.aggregate_id,
		date_diff('second', accepted_order_timestamp,fulfilled_orders_timestamp) AS processing_time 
	FROM accepted_orders ao 
	INNER JOIN fulfilled_orders co ON ao.aggregate_id=co.aggregate_id
)
SELECT * FROM processing_time