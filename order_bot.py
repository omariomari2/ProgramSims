from typing import List, Optional
from interfaces import EmailProvider, CRMProvider, InventoryProvider, Order

class OrderBot:
    def __init__(self, email_service: EmailProvider, crm_service: CRMProvider, inventory_service: InventoryProvider):
        self.email_service = email_service
        self.crm_service = crm_service
        self.inventory_service = inventory_service

    def process_orders(self):
        orders = self.email_service.get_unread_emails()
        for order in orders:
            self._handle_order(order)

    def _handle_order(self, order: Order):
        customer_status = self.crm_service.get_customer_status(order.customer_id)
        
        if customer_status != "Active":
            self.email_service.send_email(
                to_address="sales@example.com",
                subject=f"Order Exception: Customer {order.customer_id}",
                body=f"Order rejected. Customer status: {customer_status}"
            )
            return

        for item in order.items:
            item_id = item["item_id"]
            qty = item["qty"]
            stock = self.inventory_service.check_stock(item_id)
            
            if stock < qty:
                self.email_service.send_email(
                    to_address="sales@example.com",
                    subject=f"Order Exception: Out of Stock {item_id}",
                    body=f"Order rejected. Insufficient stock for {item_id}. Requested: {qty}, Available: {stock}"
                )
                return

        for item in order.items:
            self.inventory_service.decrement_stock(item["item_id"], item["qty"])

        customer_email = self.crm_service.get_customer_email(order.customer_id)
        if customer_email:
            self.email_service.send_email(
                to_address=customer_email,
                subject="Order Confirmation",
                body="Your order has been processed successfully."
            )

        self.email_service.send_email(
            to_address="warehouse@example.com",
            subject="New Fulfillment Order",
            body=f"Please fulfill order for {order.customer_id}: {order.items}"
        )
