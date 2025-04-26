from datetime import datetime

class CustomerInfo:
     def __init__(self,id=None,name=None,sex=None,birthday=None,national=None,country=None,checkin_date=None,room_type=None,room_number=None):
         self.id = str(id) if id is not None else ""
         self.name = name if name is not None else ""
         self.sex = sex if sex is not None else ""
         # Store dates as YYYY-MM-DD strings or empty string/None
         self.birthday = self._format_date_input(birthday)
         self.national = national if national is not None else ""
         self.country = country if country is not None else ""
         self.checkin_date = self._format_date_input(checkin_date)
         self.room_type = room_type if room_type is not None else ""
         self.room_number = room_number if room_number is not None else ""

     def _format_date_input(self, date_value):
          """Helper to ensure date is stored as YYYY-MM-DD string or None/empty."""
          if isinstance(date_value, datetime):
               return date_value.strftime("%Y-%m-%d")
          elif isinstance(date_value, str) and date_value:
               # Optional: add validation here if the string is in correct format
               return date_value
          else:
               return "" # Store as empty string if None or invalid

     def haveNone(self):
          # Check if critical fields are None or empty strings
          critical_fields = [self.id, self.name, self.checkin_date, self.room_type, self.room_number]
          return any(field is None or field == "" for field in critical_fields)

     # Add this method for populating Treeview easily
     def get_values_for_treeview(self):
          """Returns a tuple of values in the correct order for Treeview display (YYYY-MM-DD)."""
          return (
              self.id, self.name, self.sex, self.birthday,
              self.national, self.country, self.checkin_date,
              self.room_type, self.room_number,
          )

     def __str__(self):
         return f"CustomerInfo(ID: {self.id}, Name: {self.name}, Checkin: {self.checkin_date})"

# Assume StaffInfo class exists in staff_information.py
# from staff_information import StaffInfo
