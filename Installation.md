> https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

```bash
C:.
│   app.py
│   init_db.py
│   library.db
│
└───templates
        login.html
        student.html
        teacher.html
```

```bash
pip install Flask requests
python init_db.py
python app.py
```
### LINE Credentials
1. Go to the [LINE Developers Console](https://developers.line.biz/console/) and log in with your normal LINE account.
2. Click **Create a New Provider** (name it "SchoolLibrary").
3. Click **Create a new channel** -> Select **Messaging API**.
4. Fill in the Bot's name (e.g., "LSMS Bot") and create it.
5. Once created, click on the **Messaging API** tab. 
    * Scroll down to the QR code and scan it with your phone to add the Bot as a friend!
6. Click on the **Basic Settings** tab.
    * Scroll to the very bottom to find **"Your user ID"** (it starts with a `U...`). Copy this.
    * *Paste this into `app.py` as your `LINE_TARGET_ID`.*
7. Click on the **Messaging API** tab again.
    * Scroll to the bottom to **"Channel access token (long-lived)"** and click **Issue**. Copy this long text.
    * *Paste this into `app.py` as your `LINE_ACCESS_TOKEN`.*

### How to send LINE alerts to a Group
Right now, the bot is sending messages to your personal `User ID` (starts with a `U`). To send to a school LINE group:
1. Invite the Bot to the LINE Group.
2. You need the **Group ID** (it starts with a `C`). 
3. Once you have the Group ID, just change `LINE_TARGET_ID = 'C...'` in `app.py`.

### Backups
Since this entire system runs strictly locally on one computer, **all the data is saved inside that one `library.db` file**.
Tell your mother (or set a reminder for yourself) to copy that `library.db` file onto a USB Flash Drive or Google Drive once a week. If the computer ever breaks, you just put that file into the folder on a new computer, and absolutely zero data is lost!

> https://www.youtube.com/watch?v=uGXUqtJPypo