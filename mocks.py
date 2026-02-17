import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from interfaces import EmailProvider, CRMProvider, InventoryProvider, Order

class MockEmailProvider(EmailProvider):
    def __init__(self):
        self.sent_emails = []
        self.inbox = [
            Order(
                customer_id="C001",
                items=[{"item_id": "ITEM001", "qty": 1}],
                timestamp=datetime.now(),
                raw_text="Order from John Smith (C001) for ITEM001 x1"
            ),
            Order(
                customer_id="C999",
                items=[{"item_id": "ITEM001", "qty": 1}],
                timestamp=datetime.now(),
                raw_text="Order from Unknown (C999) for ITEM001 x1"
            ),
            Order(
                customer_id="C002",
                items=[{"item_id": "ITEM002", "qty": 100}],
                timestamp=datetime.now(),
                raw_text="Order from Jane Doe (C002) for ITEM002 x100 (Out of Stock)"
            )
        ]

    def get_unread_emails(self) -> List[Order]:
        return self.inbox

    def send_email(self, to_address: str, subject: str, body: str) -> bool:
        email = {"to": to_address, "subject": subject, "body": body}
        self.sent_emails.append(email)
        print(f"[Email Sent] To: {to_address} | Subject: {subject}")
        return True

class MockCRMProvider(CRMProvider):
    def __init__(self, data_file: str):
        with open(data_file, 'r') as f:
            self.customers = json.load(f)

    def get_customer_status(self, customer_id: str) -> str:
        if customer_id in self.customers:
            return "Active"
        return "Unknown"

    def get_customer_email(self, customer_id: str) -> Optional[str]:
        customer = self.customers.get(customer_id)
        return customer.get("email") if customer else None

class MockInventoryProvider(InventoryProvider):
    def __init__(self):
        self.inventory = {
            "ITEM001": 50,
            "ITEM002": 10
        }

    def check_stock(self, item_id: str) -> int:
        return self.inventory.get(item_id, 0)

    def decrement_stock(self, item_id: str, quantity: int) -> bool:
        current_stock = self.check_stock(item_id)
        if current_stock >= quantity:
            self.inventory[item_id] -= quantity
            return True
        return False
