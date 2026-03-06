from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "medtrack"

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["medtrack"]

users = db["users"]
appointments = db["appointments"]
diagnosis = db["diagnosis"]

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = users.find_one({"email": email, "password": password})

        if user:

            session["user"] = user["name"]
            session["role"] = user["role"]

            role = user["role"]

            if role == "admin":
                return redirect('/admin_dashboard')

            elif role == "doctor":
                return redirect('/doctor_dashboard')

            elif role == "patient":
                return redirect('/patient_dashboard')

            elif role == "receptionist":
                return redirect('/receptionist_dashboard')

        else:
            return "Invalid Email or Password"

    return render_template("login.html")
# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == "POST":

        users.insert_one({
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"],
            "role": request.form["role"]
        })

        return redirect('/login')

    return render_template("register.html")
# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template("admin_dashboard.html")

# ---------------- DOCTOR DASHBOARD ----------------
@app.route('/doctor_dashboard')
def doctor_dashboard():
    return render_template("doctor_dashboard.html")

# ---------------- PATIENT DASHBOARD ----------------
@app.route('/patient_dashboard')
def patient_dashboard():
    return render_template("patient_dashboard.html")

# ---------------- RECEPTIONIST DASHBOARD ----------------
@app.route('/receptionist_dashboard')
def receptionist_dashboard():
    return render_template("receptionist_das.html")

# ---------------- BOOK APPOINTMENT ----------------
@app.route('/book_appointment', methods=['GET','POST'])
def book_appointment():

    if request.method == "POST":

        patient = request.form["patient"]
        doctor = request.form["doctor"]
        date = request.form["date"]

        appointments.insert_one({
            "patient": patient,
            "doctor": doctor,
            "date": date
        })

        return redirect('/view_appointment')

    return render_template("book_appointment.html")
# ---------------- VIEW APPOINTMENT ----------------
@app.route('/view_appointment')
def view_appointment():

    data = list(appointments.find())

    return render_template("view_appointment.html", data=data)

# ---------------- DOCTOR VIEW APPOINTMENT ----------------
@app.route('/view_appointment_doctor')
def view_appointment_doctor():

    data = list(appointments.find())

    return render_template("view_appointment_doctor.html", data=data)

# ---------------- ADD DIAGNOSIS ----------------
@app.route('/add_diagnosis', methods=['GET','POST'])
def add_diagnosis():

    if request.method == "POST":

        patient_id = request.form["patient_id"]
        doctor_id = request.form["doctor_id"]
        report = request.form["report"]

        diagnosis.insert_one({
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "report": report
        })

        return redirect('/doctor_dashboard')

    return render_template("add_diagnosis.html")
# ---------------- LAB REPORT ----------------
@app.route('/lab_report')
def lab_report():
    return render_template("lab_report.html")

# ---------------- BILLING ----------------
@app.route('/billing')
def billing():
    return render_template("billing.html")

# ---------------- SEARCH RESULT ----------------
@app.route('/search_result')
def search_result():
    return render_template("search_result.html")

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)