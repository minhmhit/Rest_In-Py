from datetime import datetime

from revenue import CustomerInfo

class RevenueData(CustomerInfo):
    def __init__(self,id=None,name=None,sex=None,birthday=None,national=None,country=None,checkin_date=None,room_type=None,room_number=None,total_price: int=0):
        self.national = national if country is not None else ""
        CustomerInfo.__init__(self,id,name,sex,birthday,national,country,checkin_date,room_type,room_number)
        self.total_price = total_price

    def _format_date_input(self, date_value):
        if isinstance(date_value, datetime):
            return date_value.strftime("%Y-%m-%d")
        elif isinstance(date_value, str) and date_value:
            return date_value
        else:
            return "" # Store as empty string if None or invalid

    def haveNone(self):
        critical_fields = [self.id, self.name, self.checkin_date, self.room_type, self.room_number]
        return any(field is None or field == "" for field in critical_fields)

    def get_values_for_treeview(self):
        return (
            self.id, self.name, self.sex, self.birthday,
            self.national, self.country, self.checkin_date,
            self.room_type, self.room_number, self.total_price
        )

    def __str__(self):
        return f"RevenueData(ID: {self.id}, Name: {self.name}, Checkin: {self.checkin_date})"
