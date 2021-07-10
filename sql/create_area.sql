--
-- 都道府県名称を定義するテーブル
--
CREATE TABLE IF NOT EXISTS area (
  area_code varchar(10),
  area_name varchar(16),
  area_group1 char(2),
  PRIMARY KEY (area_code)
)