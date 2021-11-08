WITH accepted_orders AS (
	SELECT 
		id,
		aggregate_id,
		type,
		date_parse(SUBSTR(timestamp,1,19),'%Y-%m-%d %H:%i:%s') AS timestamp
	FROM "events_db"."events"
	WHERE type='order_accepted'
),
closed_orders AS (
	SELECT 
		id, 
		aggregate_id, 
		type, 
		date_parse(SUBSTR(timestamp,1,19),'%Y-%m-%d %H:%i:%s') AS timestamp 
	FROM "events_db"."events"
	WHERE type IN ('order_fulfilled', 'order_cancelled')
)
SELECT 
	ao.aggregate_id, 
	ao.type AS order_accepted, 
	ao.timestamp AS accepted_order_timestamp, 
	co.type AS order_fulfilled, 
	co.timestamp AS closed_order_timestamp 
FROM accepted_orders ao 
LEFT JOIN closed_orders co ON ao.aggregate_id=co.aggregate_id 
