insert into dashboard_measure(active, apparent, demand, day_id, month_id, node_id, time_id, year_id, datetime_str)
select 0,0,0,1,1,id, 1,1, '2013-01-01 00:00' from dashboard_node;