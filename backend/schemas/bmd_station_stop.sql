create table apps.bmd_station_stop
(
  id                 INT(10) auto_increment
    primary key,
  stop_authority     VARCHAR(6)      not null,
  stop_uid           VARCHAR(18)     not null,
  stop_id            VARCHAR(12)     not null,
  stop_name_zh       VARCHAR(64)     not null,
  stop_name_en       VARCHAR(128)    null,
  bearing            VARCHAR(3)      null,
  station_id         VARCHAR(18)     null,
  description        TEXT(65535)     null,
  city               VARCHAR(64)     null,
  city_code          VARCHAR(12)     null,
  location_city_code VARCHAR(12)     null,
  longitude          DECIMAL(18, 15) null,
  latitude           DECIMAL(18, 15) null
);

create unique index bmd_station_stop_route_uid_stop_uid_index
  on apps.bmd_station_stop (stop_uid);

