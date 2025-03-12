# thanh toán
from datetime import datetime

class Payment:
    def __init__(self, payment_id, room_id, amount, payment_date=None, description="Tiền phòng"):
        self.payment_id = payment_id
        self.room_id = room_id
        self.amount = amount
        self.payment_date = payment_date if payment_date else datetime.now()
        self.description = description
        
    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "room_id": self.room_id,
            "amount": self.amount,
            "payment_date": self.payment_date.strftime("%Y-%m-%d"),
            "description": self.description
        }
    
    def __str__(self):
        return f"Thanh toán: {self.payment_date.strftime('%d/%m/%Y')} - {self.amount}đ - {self.description}"
