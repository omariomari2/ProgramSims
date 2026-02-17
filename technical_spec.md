# OrderBot Technical Specification

## Overview
This document outlines the technical design for "OrderBot", an autonomous agent designed to automate the hardware order fulfillment process. The agent will be implemented in Python, leveraging a modular architecture to allow for easy testing and future integration with real APIs.

## Architecture
The system follows a component-based architecture where the `OrderBot` relies on abstract interfaces for all external interactions. This allows us to inject mock implementations for development and testing (POC) and swap them for real API adapters later.

### Core Components

#### 1. `OrderBot` (Main Agent)
The central controller that orchestrates the workflow.
*   **Responsibilities**: Polling for orders, validation logic, decision making, executing actions.
*   **Methods**:
    *   `process_orders()`: Main loop.
    *   `_validate_customer(customer_id)`: Checks CRM status.
    *   `_check_inventory(item_id, qty)`: Checks stock levels.

#### 2. `EmailService` (Interface)
Abstraction for email operations.
*   **Methods**:
    *   `get_unread_emails()`: Returns list of `Email` objects (parsing PDF content).
    *   `send_email(to, subject, body)`: Sends notifications.

#### 3. `CRMService` (Interface)
Abstraction for Customer Relationship Management (Salesforce).
*   **Methods**:
    *   `get_customer_status(customer_id)`: Returns status (e.g., "Active", "Hold", "Unknown").

#### 4. `InventoryService` (Interface)
Abstraction for Inventory Management (Google Sheets).
*   **Methods**:
    *   `check_stock(item_id)`: Returns current quantity.
    *   `decrement_stock(item_id, qty)`: Updates inventory.

## Data Models

### `Order`
Structure representing a parsed order.
```python
class Order:
    customer_id: str
    items: List[Dict[str, int]]  # [{'item_id': 'X', 'qty': 5}]
    timestamp: datetime
```

## Logic Flow
1.  **Trigger**: `OrderBot` polls `EmailService`.
2.  **Parse**: Extract `customer_id` and `items`.
3.  **Validate Customer**: Call `CRMService`. If invalid -> Send "Account Issue" Email -> Stop.
4.  **Check Inventory**: Call `InventoryService` for each item. If insufficient -> Send "Out of Stock" Email -> Stop.
5.  **Execute**:
    *   Call `InventoryService` to decrement stock.
    *   Call `EmailService` to send confirmation to customer.
    *   Call `EmailService` to send fulfillment order to warehouse.
    *   Log success.

## Proof of Concept (POC) Strategy
To validate this design without external dependencies, we will implement **Mocks**:
*   `MockEmailService`: Returns pre-defined email scenarios (Valid Order, Bad Customer Order, Out of Stock Order).
*   `MockCRMService`: Loads data from `customers_export.json` effectively acting as the Salesforce database.
*   `MockInventoryService`: Uses a simple in-memory dictionary or local CSV.

## Verification
A dedicated test suite `test_order_bot.py` will run the POC scenarios to verify that the `OrderBot` correctly handles:
1.  **Happy Path**: Order confirmed, inventory updated.
2.  **Unknown Customer**: Rejection email sent.
3.  **Inventory Shortage**: Alert email sent.
