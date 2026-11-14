from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'fy-uni-bus-secret-2026'

# ========== بيانات PythonAnywhere - عدلها باسمك ==========
# مثال: لو اسم حسابك ahmed123
# host = "ahmed123.mysql.pythonanywhere-services.com"
# user = "ahmed123"
# database = "ahmed123$fy_uni_bus"

DB_HOST = "اسمك.mysql.pythonanywhere-services.com"
DB_USER = "اسمك"
DB_PASS = "باسوردك-في-PythonAnywhere"
DB_NAME = "اسمك$fy_uni_bus"

def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

# ---------- الرئيسية + الحجز ----------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        route = request.form['route']
        trip_type = request.form['trip_type']
        trip_date = request.form['date']
        transfer_number = request.form['transfer_number']

        db = get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO bookings
            (student_name, student_phone, route, trip_date, trip_type, transfer_number, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'pending')
        """, (name, phone, route, trip_date, trip_type, transfer_number))
        db.commit()
        cur.close()
        db.close()
        return """
        <div style="text-align:center; font-family:Tahoma; padding:40px; direction:rtl;">
            <h1>تم استلام حجزك ✅</h1>
            <p style="font-size:20px;">حول على فودافون كاش: <b style="color:red;">01011112222</b></p>
            <p>هنأكد حجزك أول ما التحويل يوصل</p>
            <br><a href="/" style="background:#0a2a7a; color:#fff; padding:12px 25px; border-radius:20px; text-decoration:none;">ارجع للرئيسية</a>
        </div>
        """
    return render_template('index.html')

# ---------- تسجيل حساب ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        college = request.form['college']
        route = request.form['route']

        db = get_db()
        cur = db.cursor()
        try:
            cur.execute("""
                INSERT INTO students (name, phone, password, college, route)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, phone, password, college, route))
            db.commit()
        except:
            cur.close()
            db.close()
            return "الرقم ده مسجل قبل كده! <a href='/login'>سجل دخول</a>"
        cur.close()
        db.close()
        return redirect('/login')
    return render_template('register.html')

# ---------- دخول ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM students WHERE phone=%s AND password=%s", (phone, password))
        user = cur.fetchone()
        cur.close()
        db.close()

        if user:
            session['user'] = user['name']
            session['phone'] = user['phone']
            return redirect('/')
        else:
            return "رقم أو كلمة سر غلط! <a href='/login'>حاول تاني</a>"
    return render_template('login.html')

# ---------- لوحة الأدمن ----------
@app.route('/admin')
def admin():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM bookings ORDER BY created_at DESC")
    bookings = cur.fetchall()

    cur.execute("SELECT COUNT(*) as total FROM bookings")
    total = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as c FROM bookings WHERE status='paid'")
    paid = cur.fetchone()['c']
    cur.execute("SELECT COUNT(*) as c FROM bookings WHERE status='pending'")
    pending = cur.fetchone()['c']
    cur.execute("SELECT COUNT(*) as c FROM bookings WHERE status='cancelled'")
    cancelled = cur.fetchone()['c']

    cur.close()
    db.close()
    return render_template('admin.html', bookings=bookings, total=total, paid=paid, pending=pending, cancelled=cancelled)

@app.route('/admin/confirm/<int:booking_id>')
def confirm_booking(booking_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE bookings SET status='paid' WHERE id=%s", (booking_id,))
    db.commit()
    cur.close()
    db.close()
    return redirect('/admin')

@app.route('/admin/cancel/<int:booking_id>')
def cancel_booking(booking_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE bookings SET status='cancelled' WHERE id=%s", (booking_id,))
    db.commit()
    cur.close()
    db.close()
    return redirect('/admin')

# PythonAnywhere بيستخدم ملف WSGI مش app.run
# الكود ده عشان يشتغل على جهازك بس
if __name__ == '__main__':
    app.run(debug=True)