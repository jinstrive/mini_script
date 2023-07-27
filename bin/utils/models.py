# coding: utf-8
from utils.constants import XCX_BRANDS


class RoomRecordBuilder:

    def __init__(self, brand, ref_id, date_str) -> None:
        self.brand_id = XCX_BRANDS[brand]['brand_id']
        self.brand_name = XCX_BRANDS[brand]['brand_name']
        self.room_ref_id = ref_id
        self.date_text =  date_str

       

