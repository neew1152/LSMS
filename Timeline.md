# Day 01 | 2026-05-07

```markdown
LSMS: Simple Library System for my Mother's School

Internet: LINE Chat Group Alerts (Borrow/Return)

Local:
"
Web App Frontend
Student/Teacher Login
Library Database (Book name/ID, Username, Logs)
"

How this works:
"
Students login and enter the ID of the book they wish to borrow (safety logout if no interaction in 10 minutes) and submit to the system.

The system saves daily logs and sends alerts to LINE.

Students login, click the checkbox for the books they borrowed, and then click return.

Teachers login and can view all logs by selecting a specific date.
"

Everything happens on just one computer, let's planning (just plan!)
```
```markdown
### Phase 1: Tech Stack Selection (The Tools)
Since this runs on a single computer, we don't need heavy cloud servers. 
*   **Database:** **SQLite**. It’s perfect because it requires absolutely zero installation or server setup. It just saves as a local file on the computer.
*   **Backend (Local Server):** **Python (Flask)** or **Node.js (Express)**. Both are lightweight and can easily host a local web app (`http://localhost:5000`) and handle database logic.
*   **Frontend (User Interface):** Standard **HTML, CSS, and plain JavaScript**. We can use a simple CSS framework like Bootstrap to make it look clean and professional without much effort.
*   **Internet API:** **LINE Messaging API**. *(Note: LINE Notify is shutting down in March 2025, so we will plan to use a basic LINE Bot hooked to the Messaging API to send group messages).*

### Phase 2: Database Design (The Structure)
We need three simple tables in our SQLite database:

1.  **Users Table**
    *   `ID` (Primary Key - e.g., Student ID or Teacher ID)
    *   `Name`
    *   `Role` (Student or Teacher)
    *   `Password/PIN` (Keep it simple, maybe a 4-digit PIN for primary school students)
2.  **Books Table**
    *   `Book_ID` (Primary Key - likely a barcode number or sticker on the book)
    *   `Title`
    *   `Status` (Available / Borrowed)
3.  **Logs Table (Transactions)**
    *   `Log_ID` (Primary Key)
    *   `User_ID` (Who)
    *   `Book_ID` (What)
    *   `Action` (Borrow / Return)
    *   `Timestamp` (Date & Time)

### Phase 3: User Flows & Features (How it works)

**Flow 1: The Login System**
*   User opens the web browser on the computer.
*   They select their role (Student/Teacher), enter their ID and PIN.
*   The system routes them to either the Student Dashboard or Teacher Dashboard.

**Flow 2: Student Dashboard (Borrow & Return)**
*   **Security:** A JavaScript timer starts counting to 10 minutes (600,000 milliseconds). If the mouse moves or keys are pressed, the timer resets. If it hits 10 minutes, the app automatically redirects to the login screen.
*   **Borrowing:** 
    *   A simple text box: "Enter Book ID".
    *   Student types/scans the ID and clicks "Borrow".
    *   System checks if the book is available -> Updates Database -> Triggers LINE Alert.
*   **Returning:**
    *   The screen displays a list of books *currently* borrowed by this specific student.
    *   Each book has a checkbox next to it.
    *   Student checks the box(es) of the book(s) they are holding, and clicks "Return".
    *   System updates Database -> Triggers LINE Alert.

**Flow 3: Teacher Dashboard (Monitoring)**
*   Teacher logs in.
*   They see a simple Date Picker (e.g., "Select Date: YYYY-MM-DD").
*   Upon selecting a date, a table appears showing all daily logs: *Time | Student Name | Book Title | Action (Borrowed/Returned)*.

### Phase 4: LINE Chat Integration (The Alerts)
The only time the system needs the internet is right after a student clicks "Borrow" or "Return".
*   You will create a LINE Official Account (Bot) and invite it to the School's LINE Group.
*   When a database transaction succeeds, the local server sends a quick message to the group.
*   *Format Example:* "📚 [LSMS Alert] Student: John Doe has BORROWED 'The Little Prince' at 10:15 AM."

### Phase 5: Setup & Operation on the Single Computer
Since this is local, how will it actually run day-to-day?
1.  **Start-up Script:** We will create a simple `.bat` (Windows) or `.sh` (Mac) file on the computer's desktop. Your mother just double-clicks this icon in the morning. It starts the local server in the background.
2.  **Kiosk Mode Browser:** The script will automatically open Google Chrome in "Kiosk Mode" (full screen, no address bar) pointing directly to the local app interface.
3.  **Backups:** Since SQLite is just one file (e.g., `library.db`), we can set up a script to automatically copy this file to a USB drive or Google Drive folder once a week so your mother never loses her data.
```

> https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

> python
```markdown
### Step 1: Project Setup

LSMS/
│
├── templates/
│   └── login.html
│
├── init_db.py
└── app.py

pip install Flask

### Step 2: Database Setup (`init_db.py`)
This script will create your SQLite database file and add some dummy data so we can test the login.

### Step 3: The Web Server (`app.py`)
This is the "brain" of your app. It handles the web pages and connects to the database. 

### Step 4: The Login Page (`templates/login.html`)
This is what the students and teachers will see. I added a little bit of CSS to make it look clean and centered on the screen.

### How to test it right now:
1. Open your terminal in the `LSMS` folder.
2. Run the database script: `python init_db.py`
3. Start the server: `python app.py`
4. Open your web browser and go to: `http://127.0.0.1:5000`
5. Try logging in as the student (`ID: S01`, `PIN: 1234`) or the teacher (`ID: T01`, `PIN: 0000`).
```

```bash
C:\LSMS>python app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 700-416-386
127.0.0.1 - - [07/May/2026 17:33:55] "GET / HTTP/1.1" 500 -
Traceback (most recent call last):
  File "C:\Program Files\Python310\lib\site-packages\flask\app.py", line 1536, in __call__
    return self.wsgi_app(environ, start_response)
  File "C:\Program Files\Python310\lib\site-packages\flask\app.py", line 1514, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Program Files\Python310\lib\site-packages\flask\app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Program Files\Python310\lib\site-packages\flask\app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Program Files\Python310\lib\site-packages\flask\app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Program Files\Python310\lib\site-packages\flask\app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
  File "C:\LSMS\app.py", line 38, in login
    return render_template('login.html')
  File "C:\Program Files\Python310\lib\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Program Files\Python310\lib\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
  File "C:\Program Files\Python310\lib\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
  File "C:\Program Files\Python310\lib\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Program Files\Python310\lib\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
  File "C:\Program Files\Python310\lib\site-packages\flask\templating.py", line 66, in get_source
    return self._get_source_fast(environment, template)
  File "C:\Program Files\Python310\lib\site-packages\flask\templating.py", line 100, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: login.html
127.0.0.1 - - [07/May/2026 17:33:56] "GET /?__debugger__=yes&cmd=resource&f=style.css HTTP/1.1" 304 -
127.0.0.1 - - [07/May/2026 17:33:56] "GET /?__debugger__=yes&cmd=resource&f=debugger.js HTTP/1.1" 304 -
127.0.0.1 - - [07/May/2026 17:33:56] "GET /?__debugger__=yes&cmd=resource&f=console.png&s=t1Zx4EY37QP5lfJH9nDr HTTP/1.1" 200 -
```
```markdown
If you look at the bottom of the error text, you will see this line:
`jinja2.exceptions.TemplateNotFound: login.html`

This means Flask is looking for the `login.html` file but cannot find it. By default, Flask **strictly requires** HTML files to be inside a folder named exactly `templates` (all lowercase, with an "s" at the end).

Here are the 3 most common reasons this happens. Please check these in your `C:\LSMS` folder:

### 1. Is the folder named correctly?
Make sure you have a folder named exactly **`templates`** inside your `LSMS` folder. 
*(If it is named `template` without the "s", or capitalized like `Templates`, Flask will ignore it).*

### 2. Is the file inside the folder?
Make sure `login.html` is moved **inside** the `templates` folder, not sitting next to `app.py`.

### 3. Did Windows hide the file extension? (The "Notepad Trap")
If you created the file using Notepad on Windows, it might have accidentally saved it as `login.html.txt`. 
*   **To fix this:** Open your `templates` folder, click on **View** at the top of the file explorer, and check the box that says **"File name extensions"**. 
*   If your file is named `login.html.txt`, simply rename it and delete the `.txt` part.
```

```bash
C:\LSMS>tree /f
Folder PATH listing
Volume serial number is 9462-F902
C:.
│   app.py
│   init_db.py
│   library.db
│
└───tempates
        login.html
```
```markdown
If you look closely at your folder name:
**`tempates`**

It is missing the letter **"l"**! Flask is very strict and is looking for **`templates`**.
```

> Rollback to Ln 123

> `Welcome Student: Alice! (Dashboard coming next)`
```markdown
Now, let's build the **Student Dashboard**. We need to update `app.py` to handle the borrowing and returning logic, and create a new HTML file for the student interface (which will include the **10-minute auto-logout**).

### Step 1: Update `app.py`
We need to replace the placeholder `/student` route and add two new routes: one for borrowing, and one for returning.

### Step 2: Create `student.html` (The Dashboard)
Inside your `templates` folder, create a new file named `student.html` and paste the following code. 
```

> It's already login and I can't logout, After `B01` nothing in `Return Books`
```markdown
1. **The Logout issue**: Sometimes putting a `<button>` inside an `<a>` tag (link) causes web browsers to ignore the click. We will fix that easily.
2. **The Missing Book issue**: The database query I wrote to check *who* borrowed the book by looking at the logs was too complex and is failing to find your name. 
```

```text
"
127.0.0.1 - - [07/May/2026 17:57:04] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [07/May/2026 17:57:04] "GET /favicon.ico HTTP/1.1" 404 -
127.0.0.1 - - [07/May/2026 17:57:05] "GET /logout HTTP/1.1" 302 -
127.0.0.1 - - [07/May/2026 17:57:05] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [07/May/2026 17:57:12] "POST /borrow HTTP/1.1" 302 -
127.0.0.1 - - [07/May/2026 17:57:12] "GET / HTTP/1.1" 200 -
"
Still the same
```
```markdown
Here is what your logs show:
1. `17:57:05 GET /logout` -> The system logged you out and cleared your session.
2. `17:57:12 POST /borrow` -> You tried to borrow `B01`.
3. `17:57:12 GET /` -> Because you were already logged out, the server's security blocked the borrow request and kicked you to the Login page (`/`).

**Why did this happen? There are two common reasons:**
1. **The Timer:** Did you leave the auto-logout timer at `5000` (5 seconds) from our last test? If so, the system is logging you out in the background before you even have time to borrow the book! 
2. **The "Back" Button Ghost:** If you clicked "Logout", and then hit the **Back arrow** on your web browser, the browser shows you the Student page from its memory. But the server *knows* you logged out. So when you submit the book, it rejects it.
```

> I said it's already login, and it still the same
```markdown
Here is the secret hiding in your logs:
You went to `GET /` (the Login page), but then you instantly clicked `POST /borrow`. 

**Why is this happening?**
You accidentally pasted the **Student Dashboard code** into your **`login.html`** file! 

Because of this, when you open the app, it shows you the Student Dashboard right away (which is why you said *"It's already login"*). But because you didn't actually type your ID and PIN, the server's "brain" doesn't know who you are. 
* When you click **Borrow**, the server says *"Wait, you aren't logged in!"* and kicks you back to the login page... but your login page looks exactly like the Student Dashboard! So it looks like nothing happened.
* When you click **Logout**, the server clears your data and sends you to the login page... which again, looks like the Student Dashboard! So you *"can't logout"*.
```

> Rollback to Ln 221

My productivity has decreased. I guess I just finished playing video games and lack of sleep. And I was also using my mom's Google Account AI Studio quota, which was done through a remote device, so it wasn't very stable.

> Everything works
> 
> Now let's build the **Teacher Dashboard**. This is where your mother or other teachers can log in, pick a date, and see exactly who borrowed or returned what.

> We let it display everything first, and then let the teacher select specific dates if they think it's overwhelming.
```markdown
That makes total sense! If the school isn't doing hundreds of transactions a day, it's much easier for the teacher to just log in and see a running list of *everything*, and only use the date filter if the list gets too long.

To do this, we need to make two changes:
1. Update `app.py` so it fetches **all** logs by default, unless a specific date is chosen.
2. Update `teacher.html` to add a **"Date" column** to the table (since we are now viewing multiple days at once), and add a **"Show All"** button to clear the filter.
```

> Teachers can add or remove Logs, book names/IDs, and user (student/teacher) accounts (prevent self-deletion) directly within the UI.
```markdown
To keep the UI clean and not overwhelming, we will use a **Tabbed Interface** (Logs | Books | Users). 

We also need to use a `LEFT JOIN` in our database query so that if a teacher deletes a book or a user, the old logs don't crash (they will just show as "Deleted").
```

```bash
127.0.0.1 - - [07/May/2026 20:25:15] "GET /teacher HTTP/1.1" 500 -
Traceback (most recent call last):
  File "C:\Program Files\Python310\lib\site-packages\flask\app.py", line 1536, in __call__
    return self.wsgi_app(environ, start_response)
  File "C:\Program Files\Python310\lib\site-packages\flask\app.py", line 1514, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Program Files\Python310\lib\site-packages\flask\app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Program Files\Python310\lib\site-packages\flask\app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Program Files\Python310\lib\site-packages\flask\app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Program Files\Python310\lib\site-packages\flask\app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
  File "C:\LSMS\app.py", line 154, in teacher_dashboard
    return render_template('teacher.html', name=session['user_name'],
  File "C:\Program Files\Python310\lib\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Program Files\Python310\lib\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
  File "C:\Program Files\Python310\lib\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
  File "C:\Program Files\Python310\lib\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Program Files\Python310\lib\site-packages\jinja2\loaders.py", line 138, in load
    code = environment.compile(source, name, filename)
  File "C:\Program Files\Python310\lib\site-packages\jinja2\environment.py", line 771, in compile
    self.handle_exception(source=source_hint)
  File "C:\Program Files\Python310\lib\site-packages\jinja2\environment.py", line 942, in handle_exception
    raise rewrite_traceback_stack(source=source)
  File "C:\LSMS\templates\teacher.html", line 70, in template
    {% if selected_date %><a href="/teacher" class="btn-gray">Show All</a>{% endif %}
jinja2.exceptions.TemplateSyntaxError: unexpected '>'
127.0.0.1 - - [07/May/2026 20:25:15] "GET /teacher?__debugger__=yes&cmd=resource&f=style.css HTTP/1.1" 304 -
127.0.0.1 - - [07/May/2026 20:25:15] "GET /teacher?__debugger__=yes&cmd=resource&f=debugger.js HTTP/1.1" 304 -
127.0.0.1 - - [07/May/2026 20:25:15] "GET /teacher?__debugger__=yes&cmd=resource&f=console.png&s=uyXpLSR6v8lLEmicjTOM HTTP/1.1" 200 -
```
> You've reached your rate limit. Please try again later. Learn more

# Day 02 | 2026-05-08

```markdown
This is a **Jinja syntax error**! Sometimes, when Jinja template tags (like `{% if %}`) are placed on the exact same line as HTML tags (like `<a>`), Python gets confused during the copy-paste process or your code editor accidentally auto-completes an extra `>` character.
```

> I clicked on the book or user, and it moved to the bottom because the logs are still at the top, it won't disappear.
```markdown
This usually happens if a small piece of CSS gets accidentally deleted, or a `</div>` tag goes missing. 

There is also a **second issue** you will likely run into: Right now, if you delete a book or user, the page refreshes and kicks you back to the "Logs" tab automatically, which is very annoying!

Let's fix **both** of these problems at once. We will use JavaScript to force the tabs to hide properly, and we will add a "memory" feature so the page remembers which tab you were on even after you add or delete something.
```

> A book may have multiple copies of the same title, but each ID will be unique, and preventing bugs when they add duplicated.
```markdown
Because of how we set up the database earlier, **the system already allows duplicate titles**, and it uses the `book_id` as the only unique identifier. 

However, to make the UI better for your mother and to **completely prevent bugs if a teacher accidentally types an ID that already exists**, we can make two quick improvements to `app.py`:
1. We will update the database query so the Books table automatically groups identical titles together alphabetically.
2. We will add a strict "check" before adding a book, so if they accidentally scan the same barcode twice, it safely warns them without crashing.

### Why this is great:
1. **Try adding duplicates:** If your mother accidentally adds `B01` again, instead of throwing a scary Python error, the system safely stops her and says: *"❌ Error: ID 'B01' is already used by 'The Little Prince'. Each copy needs a unique ID!"*
2. **Try adding copies:** If she adds `B02` = "Harry Potter" and `B03` = "Harry Potter", the system happily accepts both. 
3. **Visual Grouping:** When she looks at the "Manage Books" tab, all copies of "Harry Potter" will be stacked neatly on top of each other so she can easily see how many copies the library owns.
```

> LSMS-STABLE-v0.2.0.tar

> Translate UI to Thai. (Just UI!)
```markdown
Here are the translated HTML files. I have carefully translated all the visible text, table headers, buttons, and even the JavaScript pop-up messages into polite and clear Thai, suitable for a school environment.

I also fixed a small formatting issue for the Thai language (in English it added "ed" to Borrow/Return in the logs table, but in Thai, I changed it to simply say "ยืม" and "คืน").
```

> LSMS-STABLE-v0.2.5.tar

> LINE
```markdown
This is the final piece of the puzzle! We will use the **LINE Messaging API** to send automatic alerts to LINE whenever a student borrows or returns a book.

Since LINE Notify is shutting down soon, we are using the modern **LINE Bot (Messaging API)**, which is future-proof.
```

```bash
pip install requests
```

> LSMS-STABLE-v0.5.0.tar

> Works
```markdown
### 1. How to send LINE alerts to a Group (Instead of just you)
Right now, the bot is sending messages to your personal `User ID` (starts with a `U`). To send to a school LINE group:
1. Invite the Bot to the LINE Group.
2. You need the **Group ID** (it starts with a `C`). 
*(Note: LINE hides the Group ID. If you don't know how to find the Group ID, let me know and I will give you a tiny, 1-minute trick to find it!)*
3. Once you have the Group ID, just change `LINE_TARGET_ID = 'C...'` in `app.py`.

### 2. Make it a 1-Click Start for Your Mother (Windows)
Your mother shouldn't have to open a terminal and type `python app.py` every day. Let's make a shortcut for her Desktop.

### 3. Backups (Very Important!)
Since this entire system runs strictly locally on one computer, **all the data is saved inside that one `library.db` file**.
Tell your mother (or set a reminder for yourself) to copy that `library.db` file onto a USB Flash Drive or Google Drive once a week. If the computer ever breaks, you just put that file into the folder on a new computer, and absolutely zero data is lost!
```

```markdown
"
D:.
│   app.py
│   init_db.py
│   Installation.md
│   library.db
│   Start_Library.bat
│   Timeline.md
│
└───templates
        login.html
        student.html
        teacher.html
"

Write overview README.md for GitHub, (No Installation, because I already wrote)
```

> LSMS-STABLE-v1.0.0.tar

