SELECT
    d.*,
    e.*,
    TIMESTAMPDIFF(
        HOUR,
        d.START_TIME,
        IF(d.STATUS_CODE = '01', NOW(), d.END_TIME)
    ) AS DIFF_HOUR
FROM modulog.db_event_log AS d
JOIN modulog.db_event AS e ON d.EVENT_ID = e.EVENT_ID
WHERE
    (
        -- EVENT_ID 10 → 허용 24시간
        (d.EVENT_ID = 10 AND 
         TIMESTAMPDIFF(HOUR, d.START_TIME, IF(d.STATUS_CODE = '01', NOW(), d.END_TIME)) > 24)

        OR

        -- EVENT_ID 11 → 허용 20시간
        (d.EVENT_ID = 11 AND 
         TIMESTAMPDIFF(HOUR, d.START_TIME, IF(d.STATUS_CODE = '01', NOW(), d.END_TIME)) > 20)

        OR

        -- EVENT_ID 12 → 허용 20시간
        (d.EVENT_ID = 12 AND 
         TIMESTAMPDIFF(HOUR, d.START_TIME, IF(d.STATUS_CODE = '01', NOW(), d.END_TIME)) > 20)

        OR

        -- EVENT_ID 20 → 허용 12시간
        (d.EVENT_ID = 20 AND 
         TIMESTAMPDIFF(HOUR, d.START_TIME, IF(d.STATUS_CODE = '01', NOW(), d.END_TIME)) > 12)

        OR

        -- EVENT_ID 31 → 허용 2시간
        (d.EVENT_ID = 31 AND 
         TIMESTAMPDIFF(HOUR, d.START_TIME, IF(d.STATUS_CODE = '01', NOW(), d.END_TIME)) > 2)

        OR

        -- EVENT_ID 37 → 허용 2시간
        (d.EVENT_ID = 37 AND 
         TIMESTAMPDIFF(HOUR, d.START_TIME, IF(d.STATUS_CODE = '01', NOW(), d.END_TIME)) > 2)

        OR

        -- EVENT_ID 133 → 허용 3시간
        (d.EVENT_ID = 133 AND 
         TIMESTAMPDIFF(HOUR, d.START_TIME, IF(d.STATUS_CODE = '01', NOW(), d.END_TIME)) > 3)

        OR

        -- 그 외 EVENT_ID → 허용 1시간
        (d.EVENT_ID NOT IN (10, 11, 12, 20, 31, 37, 133)
         AND TIMESTAMPDIFF(HOUR, d.START_TIME, IF(d.STATUS_CODE = '01', NOW(), d.END_TIME)) > 1)
    )
    
    AND d.START_TIME >= DATE_SUB(NOW(), INTERVAL 7 DAY);
