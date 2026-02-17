from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Order:
    customer_id: str
    items: List[Dict[str, Any]]
    timestamp: datetime
    raw_text: str

class EmailProvider(ABC):
    @abstractmethod
    def get_unread_emails(self) -> List[Order]:
        pass

    @abstractmethod
    def send_email(self, to_address: str, subject: str, body: str) -> bool:
        pass

class CRMProvider(ABC):
    @abstractmethod
    def get_customer_status(self, customer_id: str) -> str:
        pass

    @abstractmethod
    def get_customer_email(self, customer_id: str) -> Optional[str]:
        pass

class InventoryProvider(ABC):
    @abstractmethod
    def check_stock(self, item_id: str) -> int:
        pass

    @abstractmethod
    def decrement_stock(self, item_id: str, quantity: int) -> bool:
        pass
