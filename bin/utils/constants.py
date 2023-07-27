# coding: utf-8


XCX_BRANDS = {
    'duole': {'brand_id': 1, 'brand_name': '多乐'},
    'maheyou': {'brand_id': 2, 'brand_name': '麻合友'},
    'yusanjia': {'brand_id': 3, 'brand_name': '御三家'},
    }


SQL_FIND_STORE_ID = "SELECT * FROM store WHERE brand_id = %s AND store_ref_id = '%s'"
SQL_INSERT_STORE = "INSERT INTO store (brand_id, brand_name, store_ref_id, store_name, province, city, store_address, tel, lat, lng) VALUES (:brand_id, :brand_name, :store_ref_id, :store_name, :province, :city, :store_address, :tel, :lat, :lng)"


SQL_FIND_ROOM_ID = "SELECT id, room_name FROM room WHERE store_id = %s AND room_ref_id = %s"
SQL_FIND_ALL_ROOM = "SELECT * from room"
SQL_FIND_ROOM_BY_ID = "SELECT * FROM room WHERE id = %d"
SQL_INSERT_ROOM = "INSERT INTO room (store_id, room_ref_id, room_name, price_per_hour, create_time, update_time) VALUES (:store_id, :room_ref_id, :room_name, :price_per_hour, :create_time, :update_time)"

SQL_FIND_ROOMRECORD_BY_PERIOD = "SELECT *  FROM room_record WHERE room_id = %d AND date_text = '%s' AND period_id = %d"

SQL_FIND_ROOMRECORD_BY_DATETEXT = "SELECT id, room_id, date_text, is_used FROM room_record WHERE room_id = %d AND date_text = '%s'"
SQL_SUM_ROOMRECORD_BY_DATETEXT = "SELECT sum(is_used) FROM room_record WHERE room_id = %d AND date_text = '%s'"

SQL_COUNT_ROOMRECORD_USED_BY_DATETEXT = "SELECT count(is_used) FROM room_record WHERE room_id = %d AND date_text = '%s'"
SQL_INSERT_ROOMRECORD = "INSERT INTO room_record (room_id, date_text, period_id, period_time, is_used, create_time, update_time) VALUES (:room_id, :date_text, :period_id, :period_time, :is_used, :create_time, :update_time)"

SQL_UPDATE_ROOMRECORD_BY_ID = "UPDATE room_record SET is_used = ?, update_time = ?  WHERE id = ?"

SQL_FIND_ROOMSUBTOTAL_BY_DATETEXT = "SELECT * FROM room_subtotal WHERE room_id = %d AND date_text = '%s'"
SQL_UPDATE_ROOMSUBTOTAL_BY_ID = "UPDATE room_subtotal SET price_per_hour = ?, used_hour = ?, amount = ?, update_time = ?  WHERE id = ?"
SQL_INSERT_ROOMSUBTOTAL = "INSERT INTO room_subtotal (room_id, store_id, date_text, date_week, price_per_hour, used_hour, amount, create_time, update_time) VALUES (:room_id, :store_id, :date_text, :date_week, :price_per_hour, :used_hour, :amount, :create_time, :update_time)"

SQL_FIND_ALL_ROOMSUBTOTAL = "SELECT * from room_subtotal ORDER BY date_text DESC"

