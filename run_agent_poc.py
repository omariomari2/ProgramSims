from mocks import MockEmailProvider, MockCRMProvider, MockInventoryProvider
from order_bot import OrderBot

def main():
    print("Initializing OrderBot POC...")
    
    email_service = MockEmailProvider()
    crm_service = MockCRMProvider("customers_export.json")
    inventory_service = MockInventoryProvider()
    
    bot = OrderBot(email_service, crm_service, inventory_service)
    
    print("\n[Mock Environment Setup]")
    print(f"Initial Inventory: {inventory_service.inventory}")
    print(f"Unread Emails: {len(email_service.inbox)}")
    
    print("\n[Start Processing]")
    bot.process_orders()
    
    print("\n[Post-Processing State]")
    print(f"Final Inventory: {inventory_service.inventory}")
    print(f"Sent Emails: {len(email_service.sent_emails)}")
    
    print("\n[Email Log]")
    for email in email_service.sent_emails:
        print(f"To: {email['to']} | Subject: {email['subject']}")

if __name__ == "__main__":
    main()
