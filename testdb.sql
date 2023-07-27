-- SQLite

SELECT * from store where city = '杭州市';
SELECT * from store where store_name LIKE '%测试%';
SELECT * FROM room_subtotal where store_id = 109 and used_hour != 0;
SELECT * from room;
SELECT * from room_record;


-- ALTER TABLE room_subtotal ADD store_id TEXT;

-- 分组查看房间的数据
SELECT
    store_id,
    date_text,
    date_week,
    count(room_id) AS room_num,
    SUM(amount) AS total_amount,
    SUM(used_hour) AS total_used_hour
FROM
    room_subtotal
GROUP BY
    store_id,
    date_text
ORDER BY
    date_text DESC;


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