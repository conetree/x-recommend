-- Flink SQL 模板：消费行为事件并做基础聚合
-- 实际使用前请根据你的 Flink 版本与连接器补全 WITH 参数

CREATE TABLE video_events (
  user_id STRING,
  item_id STRING,
  event_type STRING,
  ts BIGINT,
  proc_time AS PROCTIME(),
  event_time AS TO_TIMESTAMP_LTZ(ts, 0),
  WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'video_events',
  'properties.bootstrap.servers' = 'kafka:9092',
  'properties.group.id' = 'flink-video-events',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json'
);

CREATE TABLE user_5m_ctr (
  user_id STRING,
  win_start TIMESTAMP(3),
  win_end TIMESTAMP(3),
  exposure_cnt BIGINT,
  click_cnt BIGINT,
  ctr DOUBLE
) WITH (
  'connector' = 'print'
);

INSERT INTO user_5m_ctr
SELECT
  user_id,
  window_start,
  window_end,
  SUM(CASE WHEN event_type = 'expose' THEN 1 ELSE 0 END) AS exposure_cnt,
  SUM(CASE WHEN event_type = 'click' THEN 1 ELSE 0 END) AS click_cnt,
  CASE WHEN SUM(CASE WHEN event_type = 'expose' THEN 1 ELSE 0 END) = 0 THEN 0
       ELSE CAST(SUM(CASE WHEN event_type = 'click' THEN 1 ELSE 0 END) AS DOUBLE)
            / CAST(SUM(CASE WHEN event_type = 'expose' THEN 1 ELSE 0 END) AS DOUBLE)
  END AS ctr
FROM TABLE(
  TUMBLE(TABLE video_events, DESCRIPTOR(event_time), INTERVAL '5' MINUTES)
)
GROUP BY user_id, window_start, window_end;
