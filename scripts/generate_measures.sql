INSERT INTO `lennin92$endashv2`.dashboard_measure (
	day_id,
	month_id,
	node_id,
	time_id,
	year_id,
	datetime_str,
	active,
	apparent,
	demand
) 
SELECT
	DAY,
	MONTH,
	node,
	HOUR,
	YEAR,
	datetime_str,
	avg(active),
	avg(apparent),
	avg(demand)
FROM
	(
		SELECT
			d.id DAY,
			m.id MONTH,
			21 node,
			h.id HOUR,
			y.id YEAR,
			concat_ws(
				'',
				y. YEAR,
				'-',
				m.char_rep,
				'-',
				d.char_rep,
				' ',
				h.char_rep
			) AS datetime_str,
			b.WhTot active,
			b.VAhTot apparent,
			b.Pos_Watts_3ph_Av demand
		FROM
			`lennin92$endashv2`.dashboard_month m,
			`lennin92$endashv2`.dashboard_year y,
			`lennin92$endashv2`.dashboard_day d,
			`lennin92$endashv2`.dashboard_time h,
			(
				SELECT
					*
				FROM
					`lennin92$uesendash`.Agronomia
				LIMIT 200
			) b
		WHERE
			y. YEAR = 2016
		AND m.id BETWEEN 9
		AND 11
	) source
GROUP BY
	node,
	YEAR,
	MONTH,
	DAY,
	HOUR
