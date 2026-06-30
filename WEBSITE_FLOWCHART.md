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
    Q --> U{Staff User?}
    U -- Yes --> V[Admin Panel]
    U -- No --> Q
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
7. The User menu opens profile, settings, notifications, admin tools, and logout.

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
| Admin Panel | `/admin/` | Staff-only Django admin |
| Logout | `/logout/` | End the current session |

