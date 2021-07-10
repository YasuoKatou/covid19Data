CREATE TABLE IF NOT EXISTS dailly_patients (
  target_date date,
  area_code varchar(10),
  patients bigint not null,
  PRIMARY KEY (target_date, area_code)
)