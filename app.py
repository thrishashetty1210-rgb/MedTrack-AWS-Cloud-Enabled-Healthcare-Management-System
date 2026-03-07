from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import config

app = Flask(__name__)
app.secret_key = "medtrack_secret"

# MongoDB Connection
client = MongoClient(config.MONGO_URI)
db = client["medtrack"]

users = db["users"]
appointments = db["appointments"]


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------
# REGISTER
# -----------------------------
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        users.insert_one({
            "name": name,
            "email": email,
            "password": password,
            "role": role
        })

        return redirect("/login")

    return render_template("register.html")


# -----------------------------
# LOGIN
# -----------------------------
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = users.find_one({
            "email": email,
            "password": password
        })

        if user:

            session["user"] = user["name"]
            session["role"] = user["role"]

            if user["role"] == "doctor":
                return redirect("/doctor_dashboard")

            elif user["role"] == "patient":
                return redirect("/patient_dashboard")

    return render_template("login.html")


# -----------------------------
# DOCTOR DASHBOARD
# -----------------------------
@app.route("/doctor_dashboard")
def doctor_dashboard():

    if "user" not in session:
        return redirect("/login")

    # Get only appointments for the logged-in doctor
    appointments = list(db.appointments.find({
        "doctor": session["user"]
    }))

    return render_template(
        "doctor_dashboard.html",
        appointments=appointments
    )

# -----------------------------
# PATIENT DASHBOARD
# -----------------------------
@app.route("/patient_dashboard")
def patient_dashboard():

    if "user" not in session:
        return redirect("/login")

    data = list(appointments.find({
        "patient": session["user"]
    }))

    return render_template(
        "patient_dashboard.html",
        appointments=data
    )


# -----------------------------
# BOOK APPOINTMENT
# -----------------------------
@app.route("/book_appointment", methods=["GET","POST"])
def book_appointment():

    if "user" not in session:
        return redirect("/login")

    # get doctors list
    doctors = list(users.find({"role": "doctor"}))

    if request.method == "POST":

        patient = session["user"]
        doctor = request.form["doctor"]
        date = request.form["date"]

        appointments.insert_one({
            "patient": patient,
            "doctor": doctor,
            "date": date
        })

        return redirect("/view_appointment_patient")

    return render_template("book_appointment.html", doctors=doctors)


# -----------------------------
# VIEW PATIENT APPOINTMENTS
# -----------------------------
@app.route("/view_appointment_patient")
def view_appointment_patient():

    if "user" not in session:
        return redirect("/login")

    data = appointments.find({"patient": session["user"]})

    return render_template(
        "view_appointment_patient.html",
        appointments=data
    )


# -----------------------------
# VIEW DOCTOR APPOINTMENTS
# -----------------------------
@app.route("/view_appointment_doctor")
def view_appointment_doctor():

    if "user" not in session:
        return redirect("/login")

    data = list(appointments.find({
        "doctor": session["user"]
    }))

    return render_template(
        "view_appointment_doctor.html",
        appointments=data
    )


#------Search results------
# -------- SEARCH PATIENT --------
@app.route("/search", methods=["POST"])
def search():

    keyword = request.form["keyword"]

    results = list(users.find({
        "name": {"$regex": keyword, "$options": "i"},
        "role": "patient"
    }))

    return render_template(
        "search_results.html",
        results=results
    )

# Doctor add report
@app.route("/add_report/<id>", methods=["GET","POST"])
def add_report(id):

    if request.method == "POST":
        report = request.form["report"]

        appointments.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"report": report}}
        )

        return redirect("/view_appointment_doctor")

    appointment = appointments.find_one({"_id": ObjectId(id)})

    return render_template("add_report.html", a=appointment)

# -----------------------------
# CANCEL APPOINTMENT
# -----------------------------
@app.route("/cancel_appointment/<id>")
def cancel_appointment(id):

    appointments.delete_one({"_id": ObjectId(id)})

    return redirect("/patient_dashboard")
#----treat patient----
@app.route("/treat_patient/<id>", methods=["GET","POST"])
def treat_patient(id):

    if request.method == "POST":

        report = request.form["report"]
        bill = request.form["bill"]

        appointments.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "report": report,
                "bill": bill,
                "payment_status": "Pending"
            }}
        )

        return redirect("/doctor_dashboard")

    data = appointments.find_one({"_id": ObjectId(id)})

    return render_template("treat_patient.html", a=data)
#---payment-----
@app.route("/pay_bill/<id>")
def pay_bill(id):

    appointments.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"payment_status": "Paid"}}
    )

    return redirect("/patient_dashboard")
# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)