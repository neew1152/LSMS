from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = 'mother_school_secret_key'

# --- LINE API SETTINGS ---
LINE_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
LINE_TARGET_ID = 'YOUR_USER_OR_GROUP_ID' 

def send_line_alert(message):
    if LINE_ACCESS_TOKEN == 'YOUR_ACCESS_TOKEN':
        return # Do nothing if Token is not set yet
        
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    data = {
        "to": LINE_TARGET_ID,
        "messages": [{"type": "text", "text": message}]
    }
    try:
        requests.post(url, headers=headers, json=data)
    except Exception as e:
        print(f"LINE API Error: {e}")

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row # Lets us access columns by name
    return conn

# Route: Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id'].strip().upper()
        pin = request.form['pin'].strip()
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ? AND pin = ?', (user_id, pin)).fetchone()
        conn.close()

        if user:
            # Save user info in the session
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = user['role']
            
            # Send them to the right dashboard
            if user['role'] == 'student':
                return redirect(url_for('student_dashboard'))
            else:
                return redirect(url_for('teacher_dashboard'))
        else:
            flash("Invalid ID or PIN. Please try again.")
            
    return render_template('login.html')

# Placeholder for Student Dashboard
# --- Update your /student route to this: ---
@app.route('/student')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    # Find books that are currently marked 'Borrowed' AND the last person to borrow them was this student
    borrowed_books = conn.execute('''
        SELECT b.book_id, b.title 
        FROM books b 
        WHERE b.status = 'Borrowed' 
        AND (SELECT user_id FROM logs WHERE book_id = b.book_id ORDER BY log_id DESC LIMIT 1) = ?
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('student.html', name=session['user_name'], borrowed_books=borrowed_books)


# --- Add this new route for BORROWING ---
@app.route('/borrow', methods=['POST'])
def borrow_book():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    book_id = request.form['book_id'].strip().upper()
    user_id = session['user_id']
    
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE book_id = ?', (book_id,)).fetchone()
    
    if not book:
        flash("❌ Book not found! Please check the ID.")
    elif book['status'] == 'Borrowed':
        flash("❌ This book is already borrowed by someone else!")
    else:
        # 1. Mark book as borrowed
        conn.execute('UPDATE books SET status = "Borrowed" WHERE book_id = ?', (book_id,))
        # 2. Save to daily logs
        conn.execute('INSERT INTO logs (user_id, book_id, action) VALUES (?, ?, ?)', (user_id, book_id, 'Borrow'))
        conn.commit()
        
        flash(f"✅ Successfully borrowed: {book['title']}")
        
        # --- SEND LINE ALERT ---
        alert_msg = f"📚 แจ้งเตือนห้องสมุด:\nนักเรียน {session['user_name']} ได้ทำการ [ยืม] หนังสือ\n📖 '{book['title']}'"
        send_line_alert(alert_msg)
        
    conn.close()
    return redirect(url_for('student_dashboard'))


# --- Add this new route for RETURNING ---
@app.route('/return', methods=['POST'])
def return_books():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    # Get the list of checked checkboxes
    returned_book_ids = request.form.getlist('book_ids')
    user_id = session['user_id']
    
    if not returned_book_ids:
        flash("⚠️ No books selected to return.")
        return redirect(url_for('student_dashboard'))
        
    conn = get_db_connection()
    for book_id in returned_book_ids:
        # 1. Mark book as available
        conn.execute('UPDATE books SET status = "Available" WHERE book_id = ?', (book_id,))
        # 2. Save to daily logs
        conn.execute('INSERT INTO logs (user_id, book_id, action) VALUES (?, ?, ?)', (user_id, book_id, 'Return'))
    
    conn.commit()
    conn.close()
    
    flash("✅ Books successfully returned!")
    
    # --- SEND LINE ALERT ---
    alert_msg = f"✅ แจ้งเตือนห้องสมุด:\nนักเรียน {session['user_name']} ได้ทำการ [คืน] หนังสือจำนวน {len(returned_book_ids)} เล่ม"
    send_line_alert(alert_msg)
    
    return redirect(url_for('student_dashboard'))

# --- 1. UPDATE YOUR TEACHER ROUTE (Look at the "books =" line) ---
@app.route('/teacher', methods=['GET', 'POST'])
def teacher_dashboard():
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))
    
    selected_date = ""
    conn = get_db_connection()
    
    query = '''
        SELECT l.log_id, date(l.timestamp, 'localtime') as log_date, 
               time(l.timestamp, 'localtime') as log_time, 
               IFNULL(u.name, l.user_id || ' (Deleted)') as student_name, 
               IFNULL(b.title, l.book_id || ' (Deleted)') as book_title, 
               l.action 
        FROM logs l
        LEFT JOIN users u ON l.user_id = u.id
        LEFT JOIN books b ON l.book_id = b.book_id
    '''
    params = []
    
    if request.method == 'POST' and request.form.get('selected_date'):
        selected_date = request.form['selected_date']
        query += " WHERE date(l.timestamp, 'localtime') = ?"
        params.append(selected_date)
        
    query += " ORDER BY l.timestamp DESC"
    
    logs = conn.execute(query, params).fetchall()
    
    # IMPROVEMENT: Orders the list by Title first, then ID, so copies group together!
    books = conn.execute('SELECT * FROM books ORDER BY title, book_id').fetchall()
    
    users = conn.execute('SELECT * FROM users ORDER BY role, name').fetchall()
    
    conn.close()
    
    return render_template('teacher.html', name=session['user_name'], 
                           logs=logs, books=books, users=users, 
                           selected_date=selected_date, current_user_id=session['user_id'])

# --- 2. ADD all these Admin Action routes BELOW the teacher route ---

@app.route('/add_log', methods=['POST'])
def add_log():
    user_id = request.form['user_id'].strip().upper()
    book_id = request.form['book_id'].strip().upper()
    action = request.form['action']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO logs (user_id, book_id, action) VALUES (?, ?, ?)', (user_id, book_id, action))
    # Update book status automatically
    new_status = 'Borrowed' if action == 'Borrow' else 'Available'
    conn.execute('UPDATE books SET status = ? WHERE book_id = ?', (new_status, book_id))
    conn.commit()
    conn.close()
    flash("✅ Manual log added successfully!")
    return redirect(url_for('teacher_dashboard'))

@app.route('/delete_log/<int:log_id>')
def delete_log(log_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM logs WHERE log_id = ?', (log_id,))
    conn.commit()
    conn.close()
    flash("🗑️ Log deleted.")
    return redirect(url_for('teacher_dashboard'))

@app.route('/add_book', methods=['POST'])
def add_book():
    book_id = request.form['book_id'].strip().upper()
    title = request.form['title'].strip()
    
    conn = get_db_connection()
    
    # Check if the ID already exists BEFORE trying to add it
    existing_book = conn.execute('SELECT * FROM books WHERE book_id = ?', (book_id,)).fetchone()
    
    if existing_book:
        # Prevent the bug/duplicate
        flash(f"❌ Error: ID '{book_id}' is already used by '{existing_book['title']}'. Each copy needs a unique ID!")
    else:
        # Safe to add
        conn.execute('INSERT INTO books (book_id, title) VALUES (?, ?)', (book_id, title))
        conn.commit()
        flash(f"✅ Book '{title}' (ID: {book_id}) added successfully!")
        
    conn.close()
    return redirect(url_for('teacher_dashboard'))

@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
    conn.commit()
    conn.close()
    flash("🗑️ Book removed.")
    return redirect(url_for('teacher_dashboard'))

@app.route('/add_user', methods=['POST'])
def add_user():
    user_id = request.form['user_id'].strip().upper()
    name = request.form['name'].strip()
    role = request.form['role']
    pin = request.form['pin'].strip()
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (id, name, role, pin) VALUES (?, ?, ?, ?)', (user_id, name, role, pin))
        conn.commit()
        flash(f"✅ User '{name}' added successfully!")
    except sqlite3.IntegrityError:
        flash("❌ Error: A user with that ID already exists.")
    conn.close()
    return redirect(url_for('teacher_dashboard'))

@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    if user_id == session['user_id']:
        flash("❌ Security Alert: You cannot delete your own account!")
        return redirect(url_for('teacher_dashboard'))
        
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash("🗑️ User removed.")
    return redirect(url_for('teacher_dashboard'))

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Runs locally on port 5000
    app.run(debug=True, host='127.0.0.1', port=5000)