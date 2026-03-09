# Vapor Lock Recruitment Tracker

![Vapor Lock Recruitment Tracker](./main_app/static/images/1024%20Logo%20with%20BG.png)

## Overview

The **Vapor Lock Recruitment Tracker** is a Django-based web application designed to help recruiters manage the full lifecycle of alliance members in **EVE Online**.

The application allows recruiters to track applicants, recruits, active members, and former members while maintaining a historical record of recruitment decisions and membership outcomes.

Recruiters can:

- Create and manage candidate records
- Track recruitment status and membership state
- Record interview notes, ESI checks, and onboarding
- Collaborate through recruiter comment threads
- View analytics and reporting dashboards

The goal of this project was to build a **practical internal tool** that improves recruitment organization and provides visibility into alliance growth, recruitment performance, and attrition trends.

This application was built as a portfolio project while also being designed for real use within an EVE Online alliance.

---

# Getting Started

### Deployed Application

[Live Application](https://recruitmenttracker-2e9d26bd5dbd.herokuapp.com/)

### Planning Materials

[Trello Project Board](https://trello.com/b/V4l3lCLG/recruitment-tracker)

The Trello board includes:

- MVP user stories
- Wireframes
- Entity relationship diagram (ERD)
- Stretch goals and planning notes

---

# Features

### Recruitment Tracking
- Track applicants through the recruitment pipeline
- Monitor recruit progress and graduation
- Store registry numbers, timezone, and corporation information

### Recruiter Collaboration
- Recruiters can leave comments on candidate profiles
- Comment threads provide shared recruitment context

### Membership Lifecycle Management
Members can be tracked through multiple states:

- Pending
- Recruit
- Member
- Rejected
- Declined
- Left
- Kicked
- Purged

Historical records are maintained even after members leave.

### EVE Online Integration
The application integrates with the **EVE Online ESI API** to:

- Resolve character names to character IDs
- Automatically display EVE character portraits

### Search and Filtering
Recruiters can quickly locate pilots by name across multiple pages including:

- Active members
- Active recruits
- Historical records
- Attrition records

### Analytics & Reporting Dashboard
The analytics page provides insight into alliance recruitment and retention.

Reports include:

- Member and recruit totals
- Recruitment conversion rates
- Recruitment rejection rates
- Attrition breakdowns (voluntary vs involuntary)
- Membership distribution by timezone
- Member tenure distributions
- Graduation tracking
- Recruiter activity statistics
- Alliance anniversary tracking by join month

---

# Technologies Used

- **Python**
- **Django**
- **PostgreSQL**
- **HTML5**
- **CSS3**
- **JavaScript**
- **Chart.js** (for analytics visualizations)
- **EVE Online ESI API**

---

# Attributions

EVE character portraits are provided by the official EVE image server:

https://images.evetech.net

EVE API documentation:

https://esi.evetech.net

Charts are generated using:

https://www.chartjs.org/

---

# Next Steps (Planned Enhancements)

Future improvements planned for the application include:

### Recruiter Performance Metrics
Expanded statistics on recruiter activity such as:

- interviews conducted
- onboarding totals
- recruit success rates

### Advanced Analytics
Additional reporting such as:

- retention trends
- recruit graduation timelines

### Notification System
Automated alerts for:

- recruits approaching graduation
- recruits in status longer than expected
- missing required recruitment data

### Improved Dashboard Visualizations
Additional charts and visual dashboards for alliance leadership and recruitment officers.

### EVE SSO Integration
Allow recruiters to authenticate using their EVE Online accounts.

### Alliance Auth Integration
Refactor the application to be an extension for more wide-spread use beyond Vapor Lock Alliance.

---

# Author

Developed by Thomas Phillips, aka **Tribesmen**, aka FatesUnited

![Tribesmen](https://images.evetech.net/characters/1801283711/portrait?size=256)

This project was created as both a portfolio project and a functional recruitment management tool for the Vapor Lock Recruitment Team.