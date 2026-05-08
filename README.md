# 📚 LSMS: Simple Library System for my Mother's School

A lightweight, locally-hosted library management system built to simplify daily book borrowing and returning for a primary school. Designed specifically to run on a single local computer, it features a clean Thai UI, an intuitive Admin Panel for teachers, and real-time LINE Chat notifications for tracking library activity.

## ✨ Project Overview

This system was created to replace manual paper logs with a reliable digital solution that requires zero cloud infrastructure or recurring server costs. All data is securely stored locally via SQLite, while internet connectivity is only utilized to push instant activity alerts to the school's LINE Group using the LINE Messaging API.

## 🚀 Key Features

### 🎓 For Students (Borrowing & Returning)
*   **Simple PIN Login**: Students log in using their unique ID and a simple PIN.
*   **Quick Borrow**: Enter a Book ID to instantly borrow a book. Prevents borrowing books that are already taken.
*   **Checkbox Returns**: Students see a list of books they currently hold and can return them with a single click.
*   **Inactivity Security**: Automatic 10-minute session timeout (auto-logout) if the computer is left unattended.
*   **LINE Notifications**: Instantly sends a message to the school LINE Group when a book is borrowed or returned.

### 👩‍🏫 For Teachers (Admin Dashboard)
*   **Daily Logs**: View all library transactions (Borrow/Return) with a built-in Date Picker to filter history.
*   **Book Management**: Add new books or delete lost ones. Automatically handles multiple copies of the same title while preventing duplicate barcode IDs.
*   **User Management**: Add or remove student and teacher accounts directly from the UI (includes safety checks to prevent deleting your own account).
*   **Manual Override**: Teachers can manually log a borrow/return action if a student forgets to do it.

## 🛠️ Tech Stack

*   **Backend**: Python 3, Flask
*   **Database**: SQLite (Local `.db` file)
*   **Frontend**: HTML5, CSS3, Vanilla JavaScript (No heavy frameworks required)
*   **API Integration**: LINE Messaging API (Push Notifications)
*   **Localization**: Fully translated Thai User Interface

## 📂 Repository Structure

```text
LSMS/
│   app.py                # Main Flask application and server routing
│   init_db.py            # Script to initialize the SQLite database and tables
│   Installation.md       # Step-by-step setup and LINE API configuration guide
│   library.db            # Local SQLite database (Auto-generated)
│   Start_Library.bat     # Windows batch script for 1-click daily startup
│   Timeline.md           # Project development timeline and notes
│
└───templates/            # Frontend HTML templates
        login.html        # Main login screen
        student.html      # Student dashboard (Borrow/Return)
        teacher.html      # Admin dashboard (Logs/Books/Users)
```

## 📖 Documentation & Setup

*   **Installation & Setup:** Please see [`Installation.md`](Installation.md) for complete instructions on how to install dependencies, run the app, and configure the LINE Bot API.
*   **Development Timeline:** Check out [`Timeline.md`](Timeline.md) for details on the project's development phases.

## 🔐 Default Test Accounts (from `init_db.py`)

If you are running this project for the first time, the following test accounts are generated:
*   **Student:** ID: `S01` | PIN: `1234`
*   **Teacher:** ID: `T01` | PIN: `0000`
*   **Test Book:** ID: `B01` | Title: `The Little Prince`