create table apps.app_sensitive_values
(
	id INT(10) auto_increment
		primary key,
	app_name VARCHAR(48) null,
	`key` VARCHAR(48) null,
	value TEXT(65535) null
)
;

create unique index app_sensitive_values_app_name_index
	on apps.app_sensitive_values (app_name)
;

