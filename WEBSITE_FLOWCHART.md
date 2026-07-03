# SMARTPOULTRY Website Flowchart

```mermaid
flowchart TD
    A[Visitor opens SMARTPOULTRY] --> B{Authenticated?}

    B -- No --> C[Login Page]
    C --> D[Create Account]
    D --> E[Register User]
    E --> F[Dashboard]
    C --> F

    B -- Yes --> F

    F --> G[Top Navigation]

    G --> H[Dashboard]

    G --> I[Management Menu]
    I --> J[Flocks]
    I --> K[Inventory]
    I --> L[Revenue]
    I --> M[Expenses]

    G --> N[Analytics Menu]
    N --> O[Predictions]
    N --> P[Reports]

    G --> Q[User Menu]
    Q --> R[Manage Profile]
    Q --> S[Settings]
    Q --> T[Notifications]
    Q --> W[Logout]

    R --> R1[Update Name, Username, Email, Phone]
    R1 --> R

    S --> S1[Change Password]
    S --> S2[Update Notification Preferences]
    S1 --> S
    S2 --> S

    J --> API1[API: Flocks]
    K --> API2[API: Inventory]
    L --> API3[API: Revenue]
    M --> API4[API: Expenses]
    O --> API5[API: Analytics]
    P --> API6[API: Reports]
    T --> API7[API: Notifications]

    W --> C
```

## Main User Flow

1. A visitor opens the website.
2. If they are not logged in, they go to the login page.
3. New users can register, then continue to the dashboard.
4. Logged-in users use the dashboard and top navigation.
5. The Management menu opens farm operation pages.
6. The Analytics menu opens prediction and report pages.
7. The User menu opens profile, settings, notifications, and logout.

## Main Pages

| Page | URL | Purpose |
| --- | --- | --- |
| Login | `/login/` | Sign in with account credentials |
| Register | `/register/` | Create a new account |
| Dashboard | `/dashboard/` | Overview of farm metrics and charts |
| Flocks | `/flocks/` | Manage poultry flocks |
| Inventory | `/inventory/` | Track feed, medicine, and supplies |
| Revenue | `/revenue/` | Track income |
| Expenses | `/expenses/` | Track costs |
| Predictions | `/analytics/` | View analytics and predictions |
| Reports | `/reports/` | Generate and view reports |
| Manage Profile | `/profile/` | Update user profile information |
| Settings | `/settings/` | Update password and notification preferences |
| Logout | `/logout/` | End the current session |

## Use Case Diagram

![SMARTPOULTRY Use Case Diagram](SMARTPOULTRY_USE_CASE.png)

## Entity Relationship Diagram

![SMARTPOULTRY Entity Relationship Diagram](SMARTPOULTRY_ERD.png)

```mermaid
flowchart LR
    Farmer((Farm Owner / User))
    Admin((Admin))
    System[SMARTPOULTRY System]

    Farmer --> UC1[Register Account]
    Farmer --> UC3[View Dashboard]
    Farmer --> UC4[Manage Flocks]
    Farmer --> UC5[Manage Inventory]
    Farmer --> UC6[Record Revenue]
    Farmer --> UC7[Record Expenses]
    Farmer --> UC8[View Predictions]
    Farmer --> UC9[Generate Reports]
    Farmer --> UC10[Manage Profile]
    Farmer --> UC11[Update Settings]
    Farmer --> UC12[View Notifications]
    Farmer --> UC13[Logout]

    Admin --> UC2[Process Login]
    Admin --> UC3
    Admin --> UC4
    Admin --> UC5
    Admin --> UC6
    Admin --> UC7
    Admin --> UC8
    Admin --> UC9
    Admin --> UC12
    Admin --> UC14[Manage Users]
    Admin --> UC15[Manage Feedback]

    UC1 --> System
    UC2 --> System
    UC3 --> System
    UC4 --> System
    UC5 --> System
    UC6 --> System
    UC7 --> System
    UC8 --> System
    UC9 --> System
    UC10 --> System
    UC11 --> System
    UC12 --> System
    UC13 --> System
    UC14 --> System
    UC15 --> System
```

## Use Case Summary

| Use Case | Actor | Description |
| --- | --- | --- |
| Register Account | Farm Owner / User | Creates a new SMARTPOULTRY account. |
| Login | Farm Owner / User | Signs in using valid account credentials. |
| View Dashboard | Farm Owner / User | Reviews farm metrics, summaries, and charts. |
| Manage Flocks | Farm Owner / User | Adds, updates, views, or manages poultry flock records. |
| Manage Inventory | Farm Owner / User | Tracks feed, medicine, and farm supplies. |
| Record Revenue | Farm Owner / User | Adds and reviews farm income records. |
| Record Expenses | Farm Owner / User | Adds and reviews farm cost records. |
| View Predictions | Farm Owner / User | Views analytics and prediction results. |
| Generate Reports | Farm Owner / User | Creates and views farm reports. |
| Manage Profile | Farm Owner / User | Updates name, username, email, and phone number. |
| Update Settings | Farm Owner / User | Changes password and notification preferences. |
| View Notifications | Farm Owner / User | Reviews system and farm-related notifications. |
| Logout | Farm Owner / User | Ends the current authenticated session. |
| Process Login | Admin | Signs in to access administrative functions. |
| Manage Users | Admin | Views and manages registered user accounts. |
| Manage Feedback | Admin | Reviews and manages submitted user feedback. |

## Detailed Use Case: Manage Farm Operations

| Field | Details |
| --- | --- |
| Use Case Name | Manage Farm Operations |
| Primary Actor | Farm Owner / User |
| Goal | To manage daily poultry farm records from one website. |
| Preconditions | The user has an account and is logged in. |
| Trigger | The user selects an option from the Management menu. |
| Main Flow | 1. The user opens the dashboard. <br> 2. The user selects Flocks, Inventory, Revenue, or Expenses. <br> 3. The system displays the selected management page. <br> 4. The user adds, views, updates, or reviews records. <br> 5. The system saves the changes and updates the displayed data. |
| Alternative Flow | If the user is not logged in, the system redirects the user to the login page. |
| Postconditions | Farm operation records are stored and available for dashboard metrics, analytics, and reports. |
