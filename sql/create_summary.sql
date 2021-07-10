--
-- 日毎の累計感染者数を保存するテーブル
--
CREATE TABLE IF NOT EXISTS summary (
  last_update date,
  area_code varchar(10),
  total bigint not null,
  PRIMARY KEY (last_update, area_code)
)