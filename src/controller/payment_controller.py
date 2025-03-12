from model.payment import Payment

class PaymentController:
    def __init__(self, view, room_controller):
        self.view = view
        self.room_controller = room_controller
        self.payments = []
        self.next_id = 1
    
    def list_payments(self):
        self.view.show_payments(self.payments, self.room_controller.rooms)
    
    def add_payment(self, room_id, amount, description="Tiền phòng"):
        # Kiểm tra xem phòng có tồn tại không
        if not self.room_controller.get_room(room_id):
            return None
            
        payment = Payment(self.next_id, room_id, amount, description=description)
        self.payments.append(payment)
        self.next_id += 1
        return payment
    
    def delete_payment(self, payment_id):
        for i, payment in enumerate(self.payments):
            if payment.payment_id == payment_id:
                del self.payments[i]
                return True
        return False
    
    def get_payment(self, payment_id):
        for payment in self.payments:
            if payment.payment_id == payment_id:
                return payment
        return None
    
    def get_payments_by_room(self, room_id):
        return [payment for payment in self.payments if payment.room_id == room_id]