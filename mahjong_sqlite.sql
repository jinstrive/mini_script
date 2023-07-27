-- SQLite
SELECT
    id,
    room_id,
    date_text,
    period_id,
    period_time,
    is_used,
    create_time,
    update_time
FROM
    room_record;

SELECT
    id,
    room_id,
    date_text,
    period_id,
    period_time,
    is_used,
    create_time,
    update_time
FROM
    room_record
where
    room_id = 7
    and date_text = '2023-07-23'
    and period_id > 40;

select
    *
from
    room
where
    room_ref_id = '1025';

select
    *
from
    room_record
WHERE room_id not in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17);

select
    *
from
    room_subtotal
WHERE room_id not in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17);

select
    *
from
    tmp_room;

-- DELETE from room_record where room_id = 7;

SELECT
    id,
    room_id,
    date_text,
    date_week,
    price_per_hour,
    used_hour,
    amount,
    create_time,
    update_time
FROM
    room_subtotal;

SELECT
    sum(is_used)
FROM
    room_record
where
    room_id = 7
    and date_text = '2023-07-23';

SELECT
    *
FROM
    room_record
where
    room_id = 7
    and date_text = '2023-07-23';

SELECT
    count(0)
FROM
    room_record
where
    room_id = 7
    and date_text = '2023-07-23'
    and is_used = 1;

SELECT
    *
from
    room_subtotal
WHERE
    date_text = '2023-07-25';

SELECT
    *
from
    room_subtotal
WHERE
    room_id = '1';

SELECT
    *
from
    room_subtotal
ORDER BY
    date_text DESC;

SELECT
    *
FROM
    room_record
where
    room_id = '1'
    and date_text = '2023-07-24';

SELECT
    *
FROM
    room_subtotal
where
    date_text = '2023-07-27'
    AND store_id in ('209', '210')

-- 分组查看房间的数据
SELECT
    store_id,
    date_text,
    date_week,
    count(room_id) AS room_num,
    SUM(amount) AS total_amount,
    SUM(used_hour) AS total_used_hour,
    SUM(used_hour) / count(room_id) AS average_hour
FROM
    room_subtotal
WHERE
    amount > 0
    and store_id in ('209', '210')
GROUP BY
    store_id,
    date_text
ORDER BY
    date_text DESC;

select * from store where brand_id = 1;

SELECT
    *
FROM
    room_subtotal
WHERE
    store_id = 204;

select * from store where id = 204;

-- ALTER TABLE room RENAME TO tmp_room;
-- DROP TABLE room;
-- UPDATE room_record SET is_used = 0 WHERE date_text = '2023-07-24';
-- ALTER TABLE room_subtotal ADD store_id TEXT;
-- UPDATE room_subtotal
-- SET store_id = (
--   SELECT store_id
--   FROM room
--   WHERE room.id = room_subtotal.room_id
-- );

CREATE TABLE
    IF NOT EXISTS room (
        id INTEGER PRIMARY KEY AUTOINCREMENT, -- id 自增
        -- brand_id INTEGER, -- 小程序ID 初始化枚举值
        -- brand_name TEXT, -- 小程序品牌名 初始化枚举值
        store_id NUMERIC, -- 多店铺店铺ID 文本
        -- store_name TEXT, -- 多店铺店铺名称 文本
        room_ref_id TEXT, -- room_id 文本
        room_name TEXT, -- room_name 文本
        price_per_hour NUMERIC, -- price_per_hour 金额
        create_time DATETIME, -- create_time 时间
        update_time DATETIME -- update_time 时间
    );

CREATE TABLE
    IF NOT EXISTS room_subtotal (
        id INTEGER PRIMARY KEY AUTOINCREMENT, -- id 自增
        room_id INTEGER, -- 自记录的房间ID
        store_id TEXT, -- 店铺id用于统计 日期
        date_text TEXT, -- date_text 日期
        date_week NUMERIC, -- 星期
        price_per_hour NUMERIC, -- price_per_hour 金额
        used_hour NUMERIC, -- used_hour 数字
        amount NUMERIC, -- amount 金额
        create_time DATETIME, -- create_time 时间
        update_time DATETIME, -- update_time 时间
        CONSTRAINT unique_id_datetext UNIQUE (room_id, date_text)
    );

CREATE TABLE
    IF NOT EXISTS room_record (
        id INTEGER PRIMARY KEY AUTOINCREMENT, -- id 自增
        room_id INTEGER, -- 自记录的房间ID
        date_text TEXT, -- date_text 日期
        period_id INTEGER, -- 时段ID 0-47, 0 代表 00:00:00-00:30:00 依次类推 
        period_time TEXT, -- 时段,半小时记录 如 00:00-00:30
        is_used INTEGER, -- 是否预定 0 未预定， 1预定
        create_time DATETIME, -- create_time 时间
        update_time DATETIME, -- update_time 时间
        CONSTRAINT unique_id_datetext UNIQUE (room_id, date_text, period_id)
    );

CREATE TABLE
    IF NOT EXISTS store (
        id INTEGER PRIMARY KEY AUTOINCREMENT, -- id 自增
        brand_id INTEGER, -- 小程序ID 初始化枚举值
        brand_name TEXT, -- 小程序品牌名 初始化枚举值
        store_ref_id TEXT, -- 源数据的ID
        store_name TEXT, -- 店铺名称
        province TEXT, -- 省份
        city TEXT, -- 市 
        store_address TEXT, -- 详细地址
        tel TEXT, -- 电话 
        lat TEXT, -- 纬度
        lng TEXT, -- 经度 
        CONSTRAINT unique_id_brand UNIQUE (brand_id, store_ref_id)
    );

-- INSERT INTO room (id, store_id, room_ref_id, room_name, price_per_hour, create_time, update_time)
-- SELECT id, store_id, room_ref_id, room_name, price_per_hour, create_time, update_time FROM tmp_room;
-- sql 手动插入多乐的店铺数据
-- INSERT INTO store (brand_id, brand_name, store_ref_id, store_name, province, city, store_address, tel, lat, lng)
-- VALUES (1, '多乐', '177', '多乐(乐提港)旗舰店', '浙江省', '杭州市', '杭州市拱墅区万通中心C座402室', '', '', '');
-- INSERT INTO store (brand_id, brand_name, store_ref_id, store_name, province, city, store_address, tel, lat, lng)
-- VALUES (1, '多乐', '178', '多乐(善贤)旗舰店', '浙江省', '杭州市', '杭州市拱墅区时瑞大厦618室', '', '', '');
-- UPDATE room SET store_id = 210 WHERE store_id = 178;
-- UPDATE room SET store_id = 210 WHERE store_id = 178;
-- UPDATE room_subtotal SET store_id = 209 WHERE store_id = 177;
-- UPDATE room_subtotal SET store_id = 210 WHERE store_id = 178;
-- UPDATE room_record SET is_used = 0 WHERE date_text = '2023-07-24';


CREATE DATABASE mahjong_test;

SELECT
    *
FROM
    store
WHERE
    brand_id = 2;

SELECT
    *
FROM
    store
WHERE
    store_ref_id = '2685';

select
    *
from
    room_subtotal
where
    store_id = 177;

SELECT
    *
from
    room;