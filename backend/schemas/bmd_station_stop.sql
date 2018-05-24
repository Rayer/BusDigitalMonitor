create table apps.bmd_station_stop
(
	id INT(10) auto_increment
		primary key,
	stop_authority VARCHAR(6) null,
	stop_uid VARCHAR(18) null,
	stop_id VARCHAR(12) null,
	stop_name VARCHAR(64) not null,
	route_authority VARCHAR(6) null,
	route_uid VARCHAR(18) null,
	route_id VARCHAR(12) null,
	route_name VARCHAR(64) not null
)
;

create unique index bmd_station_stop_route_uid_stop_uid_index
	on apps.bmd_station_stop (route_uid, stop_uid)
;

