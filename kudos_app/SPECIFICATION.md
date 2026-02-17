# Kudos System Specification

## 1. Overview
The Kudos system is an internal web application designed to foster a culture of appreciation. It allows employees to publicly recognize their colleagues' contributions.

## 2. Functional Requirements

### 2.1 User Stories
- **US1. Give Kudos**: As a user, I want to select a colleague and write a message of appreciation so that I can recognize their work.
- **US2. View Feed**: As a user, I want to see a public feed of recent kudos messages so that I can see the positive work happening in the company.
- **US3. Admin Moderation (New)**: As an administrator, I want to be able to hide or delete inappropriate kudos messages so that the platform remains professional and positive.

### 2.2 Constraints
- **Simplicity**: The system should be lightweight and easy to use.
- **Internal Only**: No public internet access required; intranet deployment.

## 3. Technical Design

### 3.1 Architecture
- **Backend**: Python (Flask)
- **Database**: SQLite (local file database)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

### 3.2 Database Schema

#### Table: `users`
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Unique User ID |
| `username` | String | Username (e.g., 'jdoe') |
| `full_name` | String | Full Name (e.g., 'John Doe') |
| `is_admin` | Boolean | Admin flag (default: False) |

#### Table: `kudos`
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Unique Kudos ID |
| `sender_id` | Integer (FK) | ID of the user sending the kudos |
| `receiver_id` | Integer (FK) | ID of the user receiving the kudos |
| `message` | Text | The appreciation message |
| `timestamp` | DateTime | When it was sent |
| `is_visible` | Boolean | **Visibility flag for moderation** (default: True) |

### 3.3 API Endpoints

- `GET /api/users`: List all users (for selection).
- `GET /api/kudos`: Get recent visible kudos.
- `POST /api/kudos`: Submit a new kudos.
- `PUT /api/kudos/<id>/moderate`: (Admin only) Toggle visibility (`is_visible`).

## 4. UI/UX Design
- **Dashboard**: Two-column layout. Left: "Give Kudos" form. Right: "Recent Kudos" scrolling feed.
- **Moderation View**: A special view for admins showing *all* kudos (including hidden ones) with "Hide/Show" toggle buttons.
