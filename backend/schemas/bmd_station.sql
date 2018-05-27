create table apps.bmd_station
(
	authority VARCHAR(6) not null,
	station_uid VARCHAR(18) not null
		primary key,
	station_id VARCHAR(12) null,
	station_position TEXT(65535) not null,
	station_address TEXT(65535) null,
	name_tw VARCHAR(48) null,
	name_en VARCHAR(48) null,
	stop_routes MEDIUMTEXT(16777215) null,
	latitude DECIMAL(18,15) not null,
	longitude DECIMAL(18,15) not null,
	update_time DATETIME(19) null,
	version INT(10) null
)
;

