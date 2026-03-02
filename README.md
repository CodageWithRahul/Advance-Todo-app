🚀 Advanced To-Do Application

A full-featured task management system built with Python and Django to help users organize daily work efficiently.
Designed with clean backend architecture, intelligent task automation, and secure authentication.

🛠️ Tech Stack
Layer	Technology Used
Backend	Python, Django (Function-Based Views)
Frontend	HTML, CSS, JavaScript
Database	PostgreSQL
ORM	Django ORM (No raw SQL queries)
Deployment	Render Cloud
🔐 Authentication & Security

This application uses secure session-based authentication powered by Django’s built-in authentication system.

✔ Session-based login system
✔ OTP verification during registration
✔ Secure password hashing
✔ Forgot password functionality
✔ Password change option
✔ CSRF protection enabled
✔ Authenticated access control for protected routes

All database interactions are handled securely using Django ORM to prevent SQL injection risks.

📋 Core Features
🗂️ Three Types of Tasks
1️⃣ Today Tasks

Tasks created for the current day.

2️⃣ Future Tasks

Tasks scheduled for a specific future date.
They automatically appear on the assigned date.

3️⃣ Regular (Recurring) Tasks

Daily recurring tasks that are automatically added as fresh tasks every day — ideal for habits and routine work.

🔄 Intelligent Task Automation
✅ Auto-Adding Pending Tasks

If a task remains incomplete, it is automatically carried forward to the next day.
This ensures no important work gets lost.

✅ Auto-Adding Regular Tasks

Regular tasks are automatically generated daily without manual input.
This keeps recurring responsibilities consistent and structured.

📅 Task History & Tracking

✔ View tasks by specific dates
✔ Track completed and pending tasks
✔ Maintain organized daily task records
✔ Structured history management

🧠 Backend Architecture

Built using Function-Based Views (FBV)

Clean and modular project structure

Efficient database management using Django ORM

No raw SQL queries used

Optimized for scalability and maintainability

☁️ Deployment

The application is deployed on Render Cloud with:

Production-ready configuration

PostgreSQL cloud database integration

Secure environment variable management

🎯 Project Highlights

Scalable backend system

Automated recurring & pending task management

Secure session-based authentication

Clean UI and structured workflow

Production deployment with PostgreSQL

📌 Future Enhancements

Email notifications

REST API integration

UI responsiveness improvements

Task categorization & tagging system


📸 Screenshots
🔐 Login Page
<img width="1919" height="868" alt="login_page" src="https://github.com/user-attachments/assets/ce9acdca-70e4-45c7-9abb-bcdb0f768d1b" />
