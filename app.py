from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.secret_key = "medtrack_secret"

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["medtrack"]

users = db["users"]
appointments = db["appointments"]
diagnosis = db["diagnosis"]

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("home.html")


# ---------------- REGISTER ----------------



@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        role = request.form["role"]

        patient_id = None
        if role == "patient":
            patient_id = "P" + str(random.randint(1000,9999))

        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "role": role,
            "phone": request.form["phone"],
            "password": request.form["password"],
            "patient_id": patient_id
        }

        users.insert_one(data)

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # Admin login
        if email == "admin@medtrack.com" and password == "admin123":
            session["role"] = "admin"
            session["email"] = email
            return redirect("/admin")

        user = users.find_one({"email":email,"password":password})

        if user:

            session["role"] = user["role"]
            session["email"] = user["email"]

            if user["role"] == "doctor":
                return redirect("/doctor")

            elif user["role"] == "patient":
                return redirect("/patient")

    return render_template("login.html")


# ---------------- ADMIN DASHBOARD ----------------

@app.route("/admin")
def admin():

    all_users = list(users.find())
    all_appointments = list(appointments.find())

    return render_template(
        "admin_dashboard.html",
        users=all_users,
        appointments=all_appointments
    )


# Delete user

@app.route("/delete_user/<id>")
def delete_user(id):

    users.delete_one({"_id":ObjectId(id)})

    return redirect("/admin")


# ---------------- DOCTOR DASHBOARD ----------------

@app.route("/doctor")
def doctor():

    all_appointments = list(appointments.find())

    return render_template(
        "doctor_dashboard.html",
        appointments=all_appointments
    )


# ---------------- PATIENT DASHBOARD ----------------

@app.route("/patient")
def patient():

    user = users.find_one({"email":session["email"]})

    reports = list(diagnosis.find({"patient_email":session["email"]}))

    return render_template(
        "patient_dashboard.html",
        reports=reports,
        patient=user
    )


# ---------------- BOOK APPOINTMENT ----------------

@app.route("/book", methods=["GET","POST"])
def book():

    if request.method == "POST":

        data = {

            "PatientID": request.form["patient_id"],
            "patient_email": session["email"],
            "DoctorID": request.form["doctor"],
            "Date": request.form["date"],
            "Time": request.form["time"],
            "Status": "Pending"
        }

        appointments.insert_one(data)

        return redirect("/patient")

    return render_template("book_appointment.html")


# ---------------- ADD DIAGNOSIS ----------------
@app.route("/diagnosis/<id>", methods=["GET","POST"])
def add_diagnosis(id):

    appointment = appointments.find_one({"_id": ObjectId(id)})

    if request.method == "POST":

        data = {
            "AppointmentID": id,
            "DoctorID": appointment["DoctorID"],
            "PatientID": appointment["PatientID"],
            "Report": request.form["report"]
        }

        diagnosis.insert_one(data)

        # Update appointment status
        appointments.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"Status": "Completed"}}
        )

        return redirect("/doctor")

    return render_template("add_diagnosis.html", appointment=appointment)

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    app.run(debug=True)