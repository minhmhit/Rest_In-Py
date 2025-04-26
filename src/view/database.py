import mysql.connector
from datetime import datetime, date

# Assume CustomerInfo and StaffInfo are correctly imported
from customer_information import CustomerInfo
from staff_information import StaffInfo
# from staff_information import StaffInfo # Need your actual import

# Mock StaffInfo for example if needed
# try:
# except ImportError:
#     print("Warning: staff_information.py not found. Using mock StaffInfo.")
#     class StaffInfo:
#          def __init__(self, id=None, name=None, sex=None, birthday=None, role=None, username=None, password=None, permissions=None):
#              self.id = id
#              self.name = name
#              self.sex = sex
#              self.birthday = birthday
#              self.role = role
#              self.username = username
#              self.password = password
#              self.permissions = permissions
#          def haveNone(self):
#              return any(getattr(self, field) is None for field in ['id', 'name', 'username', 'password', 'role']) # Example fields
#          def __str__(self):
#              return f"StaffInfo(ID: {self.id}, Name: {self.name})"


class DB_Connector:
    def __init__(self) -> None:
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # empty by default
                database="motel",  # replace with your DB
            )
            print("Database connected successfully.")
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            self.conn = None # Ensure conn is None if connection fails

    # ------ get data from database ------
    def getStaffsFromDatabase(self):
        staffs = []
        if not self.conn or not self.conn.is_connected():
            print("DB Connection not available for getStaffs.")
            return staffs
        
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id, name, sex, birthday, role, username, password, permissions FROM staffs")
            for row in cursor.fetchall():
                # Format birthday to YYYY-MM-DD string if it's a date/datetime object
                row_list = list(row)
                if isinstance(row_list[3], (datetime, date)):
                    row_list[3] = row_list[3].strftime('%Y-%m-%d')
                staff = StaffInfo(*row_list)
                staffs.append(staff)
        except mysql.connector.Error as err:
            print(f"Error fetching staffs: {err}")
        finally:
            cursor.close()
        return staffs

    def getCustomersFromDatabase(self):
        customers = []
        if not self.conn or not self.conn.is_connected():
            print("DB Connection not available for getCustomers.")
            return customers
            
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id, name, sex, birthday, national, country, checkin_date, room_type, room_number FROM customers")
            for row in cursor.fetchall():
                # --- NEW: Convert date objects to YYYY-MM-DD strings ---
                row_list = list(row)
                # Assuming birthday is index 3, checkin_date is index 6
                if isinstance(row_list[3], (datetime, date)):
                    row_list[3] = row_list[3].strftime('%Y-%m-%d')
                if isinstance(row_list[6], (datetime, date)):
                    row_list[6] = row_list[6].strftime('%Y-%m-%d')
                # --- End NEW ---
                customer = CustomerInfo(*row_list) # Create CustomerInfo object with string dates
                customers.append(customer)
        except mysql.connector.Error as err:
            print(f"Error fetching customers: {err}")
        finally:
            cursor.close()
        return customers

    def getRevenueFromDatabase(self):
        revenue_list = []
        # Implement revenue fetching logic
        print("Placeholder for getRevenueFromDatabase")
        return revenue_list

    # ------ insert data to database ------
    def setCustomerToDatabase(self,customer_data: CustomerInfo):
        if not self.conn or not self.conn.is_connected():
            print("DB Connection not available for setCustomer.")
            return

        # check if customer_data is None or have None/empty critical fields
        if customer_data is None or customer_data.haveNone(): # Using the haveNone check from CustomerInfo example
             print("customer_data is None or has incomplete critical fields")
             return

        cursor = self.conn.cursor()
        try:
             # Dates are expected to be YYYY-MM-DD strings or None/empty strings in CustomerInfo
             # mysql.connector handles None correctly for NULL columns
             # No need for .strftime('%Y-%m-%d') here if CustomerInfo stores them as strings
             # If CustomerInfo stores datetime objects, then .strftime is needed here
             # Let's assume CustomerInfo stores YYYY-MM-DD strings or ""
             cursor.execute("""
                 INSERT INTO customers (id, name, sex, birthday, national, country, checkin_date, room_type, room_number)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
             """, (
                 customer_data.id,
                 customer_data.name,
                 customer_data.sex,
                 customer_data.birthday if customer_data.birthday else None, # Use None for empty string for DB
                 customer_data.national,
                 customer_data.country,
                 customer_data.checkin_date if customer_data.checkin_date else None, # Use None for empty string for DB
                 customer_data.room_type,
                 customer_data.room_number,
             ))
             self.conn.commit()
             print(f"Customer {customer_data.id} added to database.")
        except mysql.connector.Error as err:
            print(f"Error inserting customer: {err}")
            self.conn.rollback() # Rollback in case of error
        finally:
             cursor.close()


    def setStaffToDatabase(self,staff_data: StaffInfo):
        if not self.conn or not self.conn.is_connected():
            print("DB Connection not available for setStaff.")
            return

        if staff_data is None or staff_data.haveNone():
             print("staff_data is None or has incomplete fields")
             return

        cursor = self.conn.cursor()
        try:
            # Assume birthday is YYYY-MM-DD string or "" in StaffInfo
            cursor.execute("""
                 INSERT INTO staffs (id, name, sex, birthday, role, username, password, permissions)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
             """, (
                 staff_data.id,
                 staff_data.name,
                 staff_data.sex,
                 staff_data.birthday if staff_data.birthday else None, # Use None for empty string for DB
                 staff_data.role,
                 staff_data.username,
                 staff_data.password,
                 staff_data.permissions,
             ))
            self.conn.commit()
            print(f"Staff {staff_data.id} added to database.")
        except mysql.connector.Error as err:
            print(f"Error inserting staff: {err}")
            self.conn.rollback()
        finally:
            cursor.close()


    def setRevenueToDatabase(self):
        pass # Implement revenue insertion

    # ------ remove data from database ------
    def removeCustomerFromDatabase(self,customer_id: str): # Expect string ID
        if not self.conn or not self.conn.is_connected():
            print("DB Connection not available for removeCustomer.")
            return
            
        cursor = self.conn.cursor()
        try:
             # Use parameterized query to prevent SQL injection
             cursor.execute("""
                 DELETE FROM customers
                 WHERE id = %s;
             """, (customer_id,)) # Pass customer_id as a tuple
             self.conn.commit()
             print(f"Customer {customer_id} removed from database.")
        except mysql.connector.Error as err:
            print(f"Error removing customer {customer_id}: {err}")
            self.conn.rollback()
        finally:
            cursor.close()

    def removeStaffFromDatabase(self,staff_id: str): # Expect string ID
        if not self.conn or not self.conn.is_connected():
            print("DB Connection not available for removeStaff.")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                 DELETE FROM staffs
                 WHERE id = %s;
             """, (staff_id,)) # Pass staff_id as a tuple
            self.conn.commit()
            print(f"Staff {staff_id} removed from database.")
        except mysql.connector.Error as err:
            print(f"Error removing staff {staff_id}: {err}")
            self.conn.rollback()
        finally:
            cursor.close()

    def removeRevenueFromDatabase(self):
        pass # Implement revenue removal

    # ------ update data in database ------
    def updateCustomerInDatabase(self, customer_data: CustomerInfo):
        if not self.conn or not self.conn.is_connected():
            print("DB Connection not available for updateCustomer.")
            return

        if customer_data is None or customer_data.haveNone():
             print("customer_data is None or has incomplete critical fields")
             return

        cursor = self.conn.cursor()
        try:
            # Assume dates are YYYY-MM-DD strings or "" in CustomerInfo
            cursor.execute("""
                 UPDATE customers
                 SET name = %s,
                     sex = %s,
                     birthday = %s,
                     national = %s,
                     country = %s,
                     checkin_date = %s,
                     room_type = %s,
                     room_number = %s
                 WHERE id = %s
             """, (
                 customer_data.name,
                 customer_data.sex,
                 customer_data.birthday if customer_data.birthday else None,
                 customer_data.national,
                 customer_data.country,
                 customer_data.checkin_date if customer_data.checkin_date else None,
                 customer_data.room_type,
                 customer_data.room_number,
                 customer_data.id, # Use ID in WHERE clause
             ))
            self.conn.commit()
            print(f"Customer {customer_data.id} updated in database.")
        except mysql.connector.Error as err:
            print(f"Error updating customer: {err}")
            self.conn.rollback()
        finally:
            cursor.close()


    def updateStaffInDatabase(self, staff_data: StaffInfo):
        if not self.conn or not self.conn.is_connected():
            print("DB Connection not available for updateStaff.")
            return

        if staff_data is None or staff_data.haveNone():
             print("staff_data is None or has incomplete fields")
             return

        cursor = self.conn.cursor()
        try:
            # Assume birthday is YYYY-MM-DD string or "" in StaffInfo
            cursor.execute("""
                 UPDATE staffs
                 SET name = %s,
                     sex = %s,
                     birthday = %s,
                     role = %s,
                     username = %s,
                     password = %s,
                     permissions = %s
                 WHERE id = %s
             """, (
                 staff_data.name,
                 staff_data.sex,
                 staff_data.birthday if staff_data.birthday else None,
                 staff_data.role,
                 staff_data.username,
                 staff_data.password,
                 staff_data.permissions,
                 staff_data.id, # Use ID in WHERE clause
             ))
            self.conn.commit()
            print(f"Staff {staff_data.id} updated in database.")
        except mysql.connector.Error as err:
            print(f"Error updating staff: {err}")
            self.conn.rollback()
        finally:
            cursor.close()


    def updateRevenueInDatabase(self):
        pass # Implement revenue update

    # ------ close sql connector buffer ------
    def closeBuffer(self):
        if self.conn and self.conn.is_connected():
             try:
                self.conn.close()
                print("Database connection closed.")
             except mysql.connector.Error as err:
                print(f"Error closing database connection: {err}")
