# SMARTPOULTRY Database Documentation

## Database Information

| Item | Details |
| --- | --- |
| Database File | `db.sqlite3` |
| Database Type | SQLite |
| Project | SMARTPOULTRY |
| Purpose | Stores user accounts, farm records, flock data, inventory, revenue, expenses, reports, predictions, notifications, and feedback. |

## Entity Relationship Diagram

![SMARTPOULTRY Entity Relationship Diagram](SMARTPOULTRY_ERD.png)

## Main Database Tables

| Table | Records | Description |
| --- | ---: | --- |
| `accounts_userprofile` | 4 | Stores registered users and account profile details. |
| `core_farm` | 0 | Stores farm profile information. |
| `flocks_flock` | 2 | Stores poultry flock or batch records. |
| `inventory_inventory` | 1 | Stores feed, medicine, equipment, and supply inventory. |
| `revenue_revenue` | 1 | Stores farm income records. |
| `expenses_expense` | 1 | Stores farm cost records. |
| `reports_report` | 4 | Stores generated farm reports. |
| `analytics_prediction` | 0 | Stores prediction and forecast results. |
| `core_feedback` | 1 | Stores user feedback and admin responses. |
| `notifications_notification` | 0 | Stores user notifications. |
| `notifications_notificationpreference` | 3 | Stores notification preference settings. |
| `notifications_alert` | 0 | Stores automated farm alerts. |
| `production_productionrecord` | 0 | Stores daily production records. |
| `production_mortalityrecord` | 0 | Stores flock mortality records. |
| `production_healthrecord` | 0 | Stores flock health and vaccination records. |
| `production_breedinformation` | 0 | Stores poultry breed reference information. |
| `inventory_feedtype` | 0 | Stores feed type reference data. |
| `accounts_userrole` | 0 | Stores custom user role definitions. |

## Table Fields

### `accounts_userprofile`

Stores website user account information.

| Field | Purpose |
| --- | --- |
| `id` | Primary key |
| `username` | Login username |
| `first_name` | User first name |
| `last_name` | User last name |
| `email` | User email address |
| `phone` | User phone number |
| `role` | User role such as admin, manager, staff, or viewer |
| `farm_id` | Linked farm record |
| `is_active_user` | Indicates whether the account is active |
| `created_at` | Date and time the account was created |
| `updated_at` | Date and time the account was last updated |

### `core_farm`

Stores farm profile information.

| Field | Purpose |
| --- | --- |
| `id` | Primary key |
| `owner_id` | Linked user account that owns the farm |
| `name` | Farm name |
| `location` | Farm location |
| `established_date` | Date the farm was established |
| `contact_email` | Farm contact email |
| `contact_phone` | Farm contact phone |

### `flocks_flock`

Stores poultry flock records.

| Field | Purpose |
| --- | --- |
| `id` | Primary key |
| `flock_id` | Flock identifier shown in the system |
| `breed` | Poultry breed or type |
| `quantity` | Number of birds in the flock |
| `status` | Flock status such as active, sold, deceased, or retired |
| `date_added` | Date the flock was added |
| `expected_production_date` | Expected production date |
| `notes` | Additional flock notes |

### `inventory_inventory`

Stores farm inventory items.

| Field | Purpose |
| --- | --- |
| `id` | Primary key |
| `item_type` | Item category such as feed, medicine, equipment, or other |
| `name` | Inventory item name |
| `quantity` | Available quantity |
| `unit` | Measurement unit |
| `cost_per_unit` | Cost per unit |
| `total_value` | Total inventory value |
| `date_added` | Date the item was added |
| `last_updated` | Date the item was last updated |
| `notes` | Additional notes |

### `revenue_revenue`

Stores farm income records.

| Field | Purpose |
| --- | --- |
| `id` | Primary key |
| `flock_id` | Related flock, if applicable |
| `revenue_type` | Income category such as eggs, meat, birds, manure, or other |
| `quantity` | Quantity sold or recorded |
| `unit` | Unit of measurement |
| `price_per_unit` | Selling price per unit |
| `total_amount` | Total income amount |
| `date` | Revenue date |
| `notes` | Additional notes |

### `expenses_expense`

Stores farm expense records.

| Field | Purpose |
| --- | --- |
| `id` | Primary key |
| `expense_type` | Expense category such as feed, medicine, equipment, labor, utilities, or maintenance |
| `description` | Expense description |
| `amount` | Expense amount |
| `date` | Expense date |
| `category` | Additional category label |
| `notes` | Additional notes |

### `reports_report`

Stores generated reports.

| Field | Purpose |
| --- | --- |
| `id` | Primary key |
| `report_type` | Report type such as daily, weekly, monthly, production, or financial |
| `title` | Report title |
| `start_date` | Report start date |
| `end_date` | Report end date |
| `summary` | Report summary |
| `generated_at` | Date and time the report was generated |

### `analytics_prediction`

Stores prediction and forecast records.

| Field | Purpose |
| --- | --- |
| `id` | Primary key |
| `prediction_type` | Prediction category such as eggs, meat, profit, or expenses |
| `forecast_date` | Forecast date |
| `predicted_value` | Predicted value |
| `actual_value` | Actual value, if available |
| `accuracy_percentage` | Prediction accuracy |
| `method` | Prediction method used |

### `core_feedback`

Stores user feedback.

| Field | Purpose |
| --- | --- |
| `id` | Primary key |
| `user_id` | User who submitted the feedback |
| `subject` | Feedback subject |
| `message` | Feedback message |
| `rating` | User rating |
| `status` | Feedback status |
| `admin_response` | Admin response |

## Main Relationships

| Relationship | Description |
| --- | --- |
| `UserProfile` to `Farm` | A user can own or belong to a farm. |
| `UserProfile` to `Feedback` | A user can submit feedback. |
| `UserProfile` to `Notification` | A user can receive notifications. |
| `UserProfile` to `NotificationPreference` | A user has notification settings. |
| `Farm` to `Alert` | A farm can have automated alerts. |
| `Flock` to `Revenue` | A flock can be connected to income records. |
| `Flock` to `ProductionRecord` | A flock can have production records. |
| `Flock` to `MortalityRecord` | A flock can have mortality records. |
| `Flock` to `HealthRecord` | A flock can have health records. |

## Current Sample Records

### Flocks

| Flock ID | Breed | Quantity | Status |
| --- | --- | ---: | --- |
| `1` | layers | 13 | active |
| `2` | broilers | 12 | active |

### Inventory

| Item | Type | Quantity | Unit | Cost Per Unit | Total Value |
| --- | --- | ---: | --- | ---: | ---: |
| Chick Booster | feed | 10 | 10kg | 50 | 500 |

### Revenue

| Type | Quantity | Price Per Unit | Total Amount | Date |
| --- | ---: | ---: | ---: | --- |
| eggs | 90 | 10 | 900 | 2026-06-30 |

### Expenses

| Type | Description | Amount | Date |
| --- | --- | ---: | --- |
| feed | Chick Booster | 500 | 2026-06-30 |

### Feedback

| Subject | Message | Rating | Status |
| --- | --- | ---: | --- |
| An Excellent Job | Wonderful website | 5 | new |
