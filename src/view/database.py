import mysql.connector

from customer_information import CustomerInfo
from staff_information import StaffInfo

class DB_Connector:
    def __init__(self) -> None:
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # empty by default
            database="motel",  # replace with your DB
        )

    # ------ get data from database ------
    def getStaffsFromDatabase(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, sex, birthday, role, username, password, permissions FROM staffs")

        staffs = []
        
        for row in cursor.fetchall():
            staff = StaffInfo(*row)
            staffs.append(staff)

        cursor.close()
        return staffs

    def getCustomersFromDatabase(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, sex, birthday, national, country, checkin_date, room_type, room_number FROM customers")

        customers = []

        for row in cursor.fetchall():
            customer = CustomerInfo(*row)
            customers.append(customer)

        cursor.close()
        return customers

    def getRevenueFromDatabase(self):
        revenue_list = []
        return revenue_list

    # ------ insert data to database ------
    def setCustomerToDatabase(self,customer_data: CustomerInfo):
        # check if customer_data is None or have None field
        if customer_data is None or customer_data.haveNone():
            print("customer_data is None or has incomplete fields")
            return

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO customers (id, name, sex, birthday, national, country, checkin_date, room_type, room_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            customer_data.id,
            customer_data.name,
            customer_data.sex,
            customer_data.birthday.strftime('%Y-%m-%d'),
            customer_data.national,
            customer_data.country,
            customer_data.checkin_date.strftime('%Y-%m-%d'),
            customer_data.room_type,
            customer_data.room_number,
        ))
        cursor.close()
        self.conn.commit()

    def setStaffToDatabase(self,staff_data: StaffInfo):
        # check if staff_data is None or have None field
        if staff_data is None or staff_data.haveNone():
            print("staff_data is None or has incomplete fields")
            return

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO staffs (id, name, sex, birthday, role, username, password, permissions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            staff_data.id,
            staff_data.name,
            staff_data.sex,
            staff_data.birthday.strftime('%Y-%m-%d'),
            staff_data.role,
            staff_data.username, 
            staff_data.password,
            staff_data.permissions,
        ))
        cursor.close()
        self.conn.commit()

    def setRevenueToDatabase(self):
        pass

    # ------ remove data from database ------
    def removeCustomerFromDatabase(self,customer_id: int):
        cursor = self.conn.cursor()
        cursor.execute(f"""
            DELETE FROM customers
            WHERE id = {customer_id};
        """)
        self.conn.commit()

    def removeStaffFromDatabase(self,staff_id: int):
        cursor = self.conn.cursor()
        cursor.execute(f"""
            DELETE FROM staffs
            WHERE id = {staff_id};
        """)
        self.conn.commit()

    def removeRevenueFromDatabase(self):
        pass

    # ------ update data in database ------
    def updateCustomerInDatabase(self, customer_data: CustomerInfo):
        # check if customer_data is None or has any None fields
        if customer_data is None or customer_data.haveNone():
            print("customer_data is None or has incomplete fields")
            return

        cursor = self.conn.cursor()
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
            customer_data.birthday.strftime('%Y-%m-%d'),
            customer_data.national,
            customer_data.country,
            customer_data.checkin_date.strftime('%Y-%m-%d'),
            customer_data.room_type,
            customer_data.room_number,
            customer_data.id,
        ))
        cursor.close()
        self.conn.commit()

    def updateStaffInDatabase(self, staff_data: StaffInfo):
        # check if customer_data is None or has any None fields
        if staff_data is None or staff_data.haveNone():
            print("staff_data is None or has incomplete fields")
            return

        cursor = self.conn.cursor()
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
            staff_data.birthday.strftime('%Y-%m-%d'),
            staff_data.role,
            staff_data.username, 
            staff_data.password,
            staff_data.permissions,
            staff_data.id,
        ))
        cursor.close()
        self.conn.commit()

    def updateRevenueInDatabase(self):
        pass

    # ------ close sql connector buffer ------
    def closeBuffer(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Database connection closed.") # For debugging
