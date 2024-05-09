from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure the Application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return redirect("/login")


# Authentication Routes

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")

        # Map role to the appropriate database table
        role_to_table = {
            "admin": "admins",
            "teacher": "teachers",
            "student": "students",
        }

        # Check if the selected role is valid
        if role not in role_to_table:
            return "Select a valid role"

        table_name = role_to_table[role]

        # Query database for user
        user = db.execute(
            "SELECT * FROM :table_name WHERE username = :username",
            table_name=table_name,
            username=username,
        )

        # Check if user exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0]["password"], password):
            return render_template("message.html", msg="Incorrect Username / Password")

        # Store user information in session
        session["user_id"] = user[0]["id"]
        session["user_role"] = role

        # Redirect to the appropriate dashboard
        return redirect("/profile")

    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """User Log out"""
    if request.method == "POST":
        # Forget any user_id
        session.clear()

        # Redirect to login page
        return redirect("/login")
    else:
        # Forget any user_id
        session.clear()

        # Redirect to login page
        return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        input_values = {
            "firstname": request.form.get("firstname"),
            "lastname": request.form.get("lastname"),
            "email": request.form.get("email"),
            "institute": request.form.get("institute"),
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "confirmation": request.form.get("confirmation"),
        }
        # Check if all fields are empty or contain only whitespace
        all_fields_empty = all(
            value is None or value.strip() == "" for value in input_values.values()
        )
        if all_fields_empty:
            return render_template("message.html", msg="All fields must be filled")
        elif input_values["password"] != input_values["confirmation"]:
            return render_template(
                "message.html", msg="Password does not match with confirm password"
            )

        # Query database
        try:
            user = db.execute(
                "SELECT * FROM admins WHERE username = ?", (input_values["username"],)
            )
            if user:
                # Username is already taken; return an error message
                return render_template(
                    "message.html",
                    msg="Username is already taken, choose different one",
                )
            db.execute(
                "INSERT INTO admins (firstname, lastname, email, institute, username, password) VALUES(?, ?, ?, ?, ?, ?)",
                input_values["firstname"],
                input_values["lastname"],
                input_values["email"],
                input_values["institute"],
                input_values["username"],
                generate_password_hash(input_values["password"]),
            )
            # Forget any user_id
            session.clear()
            # Remember which user has logged in
            rows = db.execute(
                "SELECT * FROM admins WHERE username = ?", input_values["username"]
            )
            return redirect("/login")
            # session["user_id"] = rows[0]["id"]
        except Exception as e:
            print(f"Error during registration: {str(e)}")
            return render_template(
                "message.html",
                msg="An error occurred during registration. Please try again later.",
            )
    else:
        return render_template("register.html")

# Profile Route

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        ID = request.form.get("user_id")
        user = request.form.get("check_user")

        if user == "teacher":
            rows = db.execute(f"SELECT * FROM teachers WHERE id = ?", ID)
            course = db.execute(
                "SELECT courses.course_name FROM teachers JOIN courses ON teachers.course_id = courses.id WHERE teachers.id = ?",
                ID,
            )
            return render_template(
                "teacher.html",
                user=rows[0],
                course=course[0],
                role=session["user_role"],
            )
        elif user == "student":
            rows = db.execute(f"SELECT * FROM students WHERE id = ?", ID)
            course = db.execute(
                "SELECT courses.course_name FROM students JOIN courses ON students.course_id = courses.id WHERE students.id = ?",
                ID,
            )
            teacher = db.execute(
                "SELECT teachers.firstname, teachers.lastname FROM students JOIN teachers ON students.teacher_id = teachers.id WHERE students.id = ?",
                ID,
            )
            result = db.execute(
                "SELECT admins.institute FROM students JOIN admins ON students.admin_id = admins.id WHERE students.id = ?",
                ID,
            )
            if rows:
                return render_template(
                    "student.html",
                    user=rows[0],
                    access="login",
                    course=course[0],
                    teacher=teacher[0],
                    org=result[0],
                    role=session["user_role"],
                )
        else:
            return render_template("Not Found")
    else:
        # Retrieve the user's role from the session
        user_role = session.get("user_role")
        user_id = session["user_id"]

        if user_role is None:
            # Handle the case where the user is not logged in
            return redirect("/login")

        if user_role == "admin":
            rows = db.execute("SELECT * FROM admins WHERE id = ?", user_id)
            return render_template(
                f"{user_role}.html",
                user=rows[0],
                access="admin",
                role=session["user_role"],
            )
        elif user_role == "teacher":
            rows = db.execute("SELECT * FROM teachers WHERE id = ?", user_id)
            course = db.execute(
                "SELECT courses.course_name FROM teachers JOIN courses ON teachers.course_id = courses.id WHERE teachers.id = ?",
                user_id,
            )
            if rows:
                return render_template(
                    f"{user_role}.html",
                    user=rows[0],
                    access="teacher",
                    course=course[0],
                    role=session["user_role"],
                )
        elif user_role == "student":
            rows = db.execute("SELECT * FROM students WHERE id = ?", user_id)
            course = db.execute(
                "SELECT courses.course_name FROM students JOIN courses ON students.course_id = courses.id WHERE students.id = ?",
                user_id,
            )
            teacher = db.execute(
                "SELECT teachers.firstname, teachers.lastname FROM students JOIN teachers ON students.teacher_id = teachers.id WHERE students.id = ?",
                user_id,
            )
            result = db.execute(
                "SELECT admins.institute FROM students JOIN admins ON students.admin_id = admins.id WHERE students.id = ?",
                user_id,
            )
            if rows:
                return render_template(
                    f"{user_role}.html",
                    user=rows[0],
                    access="student",
                    course=course[0],
                    org=result[0],
                    teacher=teacher[0],
                    role=session["user_role"],
                )
            # Handle the case where the user's role is not recognized
            return redirect("/login")

# Execute Teachers Routes

@app.route("/classes", methods=["GET", "POST"])
@login_required
def classes():
    admin_id = session["user_id"]
    rows = db.execute(
        "SELECT courses.id, courses.course_name, teachers.firstname, teachers.lastname, courses.start_date FROM courses LEFT JOIN teachers ON courses.id = teachers.course_id WHERE courses.admin_id = ?",
        admin_id,
    )
    return render_template(
        "classes.html",
        classes=rows,
        user="admin",
        table="courses",
        role=session["user_role"],
    )


@app.route("/teachers", methods=["GET", "POST"])
@login_required
def teachers():
    if session["user_role"] != "admin":
        return redirect("/login")
    admin_id = session["user_id"]
    rows = db.execute("SELECT * FROM teachers WHERE admin_id = ?", admin_id)
    return render_template(
        "teachers.html",
        teachers=rows,
        user="teacher",
        table="teachers",
        access="admin",
        role=session["user_role"],
    )


@app.route("/student_list", methods=["GET", "POST"])
@login_required
def student_list():
    user_role = session["user_role"]
    user_id = session["user_id"]
    if user_role == "admin":
        rows = db.execute(
            "SELECT students.id, students.firstname, students.lastname, teachers.firstname AS teacher_firstname, teachers.lastname AS teacher_lastname, courses.course_name FROM students JOIN courses ON students.course_id =  courses.id JOIN teachers ON students.teacher_id = teachers.id WHERE courses.admin_id = ?",
            user_id,
        )
    elif user_role == "teacher":
        rows = db.execute(
            "SELECT students.id, students.firstname, students.lastname, teachers.firstname AS teacher_firstname, teachers.lastname AS teacher_lastname, courses.course_name FROM students JOIN courses ON students.course_id =  courses.id JOIN teachers ON students.teacher_id = teachers.id WHERE students.teacher_id = ?",
            user_id,
        )
    return render_template(
        "student_list.html",
        students=rows,
        user="student",
        table="students",
        role=user_role,
    )




@app.route("/students", methods=["GET", "POST"])
@login_required
def students():
    user_role = session["user_role"]
    user_id = session["user_id"]
    attendance_data = db.execute(
        "SELECT DISTINCT student_id FROM attendance WHERE student_id IN (SELECT id FROM students WHERE teacher_id = ?)",
        user_id,
    )
    common_sql = """
        SELECT students.id, students.firstname, students.lastname, courses.course_name, attendance.date, attendance.status
        FROM students
        JOIN courses ON students.course_id = courses.id
        LEFT JOIN attendance ON students.id = attendance.student_id
    """

    if user_role == "teacher":
        sql = f"{common_sql} WHERE students.teacher_id = ? ORDER BY students.id, attendance.date DESC"
    else:
        sql = f"{common_sql} WHERE students.admin_id = ? ORDER BY students.id, attendance.date DESC"

    rows = db.execute(sql, user_id)
    # Process the data to group it by date
    attendance_by_date = {}
    for row in rows:
        date = row["date"]
        if date not in attendance_by_date:
            attendance_by_date[date] = []
        attendance_by_date[date].append(row)
    # Create a dictionary to group attendance data by date

    return render_template(
        "students.html",
        students=rows,
        user="student",
        table="students",
        role=user_role,
        attendance_by_date=attendance_by_date,
        attendance_data=attendance_data,
    )

# Attendance Routes


@app.route("/record_students", methods=["GET", "POST"])
@login_required
def record_students():
    user_role = session["user_role"]
    user_id = session["user_id"]
    rows = db.execute(
        "SELECT DISTINCT students.id, students.firstname, students.lastname, courses.course_name "
        + "FROM students "
        + "JOIN courses ON students.course_id = courses.id "
        + "LEFT JOIN attendance ON students.id = attendance.student_id "
        + "WHERE students.teacher_id = ? "
        + "ORDER BY students.id ASC",
        user_id,
    )
    print(rows)
    return render_template(
        "record_students.html",
        students=rows,
        user="student",
        table="students",
        role=user_role,
    )

@app.route("/record_attendance", methods=["GET", "POST"])
@login_required
def record_attendance():
    if request.method == "POST":
        student_id = request.form.get("user_id")
        today = date.today()
        formatted_date = today.strftime("%Y-%m-%d")  # Format the date as needed
        # formatted_date = "2023-09-26"
        status = request.form.get("status")
        existing_attendance = db.execute(
            "SELECT * FROM attendance WHERE student_id = ? AND date = ?",
            student_id,
            formatted_date,
        )
        if not existing_attendance:
            db.execute(
                "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                student_id,
                formatted_date,
                status,
            )
            return redirect("/students")
        else:
            return render_template(
                "message.html", msg="Attendance already recorded for today"
            )
    return render_template("students.html", role=session["user_role"])



# Adding Users Routes

@app.route("/add_teacher", methods=["GET", "POST"])
@login_required
def add_teacher():
    """Register Teacher"""
    if session["user_role"] != "admin":
        return redirect("/login")
    else:
        if request.method == "POST":
            admin_id = session["user_id"]
            input_values = {
                "firstname": request.form.get("firstname"),
                "lastname": request.form.get("lastname"),
                "email": request.form.get("email"),
                "subject": request.form.get("subject"),
                "qualification": request.form.get("qualification"),
                "course_id": request.form.get("course_id"),
                "username": request.form.get("username"),
                "password": request.form.get("password"),
                "confirmation": request.form.get("confirmation"),
            }
            # Check if all fields are empty or contain only whitespace
            all_fields_empty = all(
                value is None or value.strip() == "" for value in input_values.values()
            )
            if all_fields_empty:
                return render_template("message.html", msg="All fields must be filled")
            elif not input_values["course_id"]:
                return render_template("message.html", msg="Select a class")
            elif input_values["password"] != input_values["confirmation"]:
                return render_template(
                    "message.html", msg="Password does not match with confirm password"
                )

            # Query database
            try:
                user = db.execute(
                    "SELECT * FROM teachers WHERE username = ?",
                    (input_values["username"],),
                )
                if user:
                    # Username is already taken; return an error message
                    return render_template(
                        "message.html",
                        msg="Username is already taken, choose different one",
                    )
                db.execute(
                    "INSERT INTO teachers (firstname, lastname, email, subject, qualification, username, password, course_id, admin_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    input_values["firstname"],
                    input_values["lastname"],
                    input_values["email"],
                    input_values["subject"],
                    input_values["qualification"],
                    input_values["username"],
                    generate_password_hash(input_values["password"]),
                    input_values["course_id"],
                    admin_id,
                )
            except Exception as e:
                print(f"Error during registration: {str(e)}")
                return render_template(
                    "message.html",
                    msg="An error occurred during adding teacher. Please try again later.",
                )
            return redirect("/teachers")
        else:
            rows = db.execute(
                "SELECT courses.id, courses.course_name FROM courses LEFT JOIN teachers ON courses.id = teachers.course_id WHERE teachers.id IS NULL AND courses.admin_id = ?",
                session["user_id"],
            )
            return render_template(
                "add_teacher.html", rows=rows, role=session["user_role"]
            )


@app.route("/add_student", methods=["GET", "POST"])
@login_required
def add_student():
    """Register student"""
    if session["user_role"] != "admin":
        return redirect("/login")
    else:
        if request.method == "POST":
            admin_id = session["user_id"]
            input_values = {
                "firstname": request.form.get("firstname"),
                "lastname": request.form.get("lastname"),
                "course_id": request.form.get("course_id"),
                "email": request.form.get("email"),
                "username": request.form.get("username"),
                "password": request.form.get("password"),
                "confirmation": request.form.get("confirmation"),
            }
            # Check if all fields are empty or contain only whitespace
            all_fields_empty = all(
                value is None or value.strip() == "" for value in input_values.values()
            )
            if all_fields_empty:
                return render_template("message.html", msg="All fields must be filled")
            elif input_values["password"] != input_values["confirmation"]:
                return render_template(
                    "message.html", msg="Password must match with confirm password"
                )

            # Query database
            try:
                user = db.execute(
                    "SELECT * FROM students WHERE username = ?",
                    (input_values["username"],),
                )
                if user:
                    # Username is already taken; return an error message
                    return render_template(
                        "message.html",
                        msg="Username is already taken, choose different one",
                    )

                # Query the teachers table to retrieve the teacher_id based on course_id
                teacher_id_result = db.execute(
                    "SELECT id FROM teachers WHERE course_id = ?",
                    input_values["course_id"],
                )

                if not teacher_id_result:
                    return render_template(
                        "message.html", msg="No teacher found for selected course"
                    )

                # Extract the teacher_id from the query result
                teacher_id = teacher_id_result[0]["id"]

                db.execute(
                    "INSERT INTO students (firstname, lastname, email, username, password, teacher_id, course_id, admin_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                    input_values["firstname"],
                    input_values["lastname"],
                    input_values["email"],
                    input_values["username"],
                    generate_password_hash(input_values["password"]),
                    teacher_id,
                    input_values["course_id"],
                    admin_id,
                )
            except Exception as e:
                print(f"Error during registration: {str(e)}")
                return render_template(
                    "message.html",
                    msg="An error occurred during adding student. Please try again later.",
                )

            # Redirect user to home page
            return redirect("/student_list")
        else:
            admin_id = session["user_id"]
            rows = db.execute(
                "SELECT courses.id, courses.course_name FROM courses LEFT JOIN teachers ON courses.id = teachers.course_id WHERE teachers.id IS NOT NULL AND courses.admin_id = ?",
                admin_id,
            )
            return render_template(
                "add_student.html", rows=rows, role=session["user_role"]
            )


@app.route("/add_class", methods=["GET", "POST"])
@login_required
def add_class():
    """Add Class"""
    if request.method == "POST":
        course_name = request.form.get("course_name")
        today = date.today()
        formatted_date = today.strftime("%Y-%m-%d")
        admin_Id = session["user_id"]
        if not course_name:
            return "Must provide a class name"

        # Query database
        try:
            user = db.execute(
                "SELECT * FROM courses WHERE course_name = ?", course_name
            )
            if user:
                # Class exists; return an error message
                flash("Class Name exists", "error")
                return redirect("/classes")
            db.execute(
                "INSERT INTO courses (course_name, start_date, admin_id) VALUES (?, ?, ?)",
                course_name,
                formatted_date,
                admin_Id,
            )
            flash("Added Successfully!", "success")
            return redirect("/classes")
        except Exception as e:
            print(f"Error during Adding course: {str(e)}")
            return render_template(
                "message.html",
                msg="An error occurred during adding class. Please try again later.",
            )

    else:
        return render_template("classes.html", role=session["user_role"])







# User Dashboard Route

@app.route("/admin_dashboard", methods=["GET", "POST"])
@login_required
def admin_dashboard():
    admin_id = session["user_id"]
    admin = db.execute(
        "SELECT firstname, lastname, institute FROM admins WHERE id = ?", admin_id
    )
    classes = db.execute(
        "SELECT COUNT(*) AS count FROM courses WHERE admin_id = ?", admin_id
    )
    teachers = db.execute(
        "SELECT COUNT(*) AS count FROM teachers WHERE admin_id = ?", admin_id
    )
    students = db.execute(
        "SELECT COUNT(*) AS count FROM students WHERE admin_id = ?", admin_id
    )
    return render_template(
        "admin_dashboard.html",
        role=session["user_role"],
        admin=admin[0],
        classes=classes[0]["count"],
        teachers=teachers[0]["count"],
        students=students[0]["count"],
    )


@app.route("/teacher_dashboard", methods=["GET", "POST"])
@login_required
def teacher_dashboard():
    teacher_id = session["user_id"]
    teacher = db.execute(
        "SELECT firstname, lastname, subject FROM teachers WHERE id = ?", teacher_id
    )
    students = db.execute(
        "SELECT COUNT(*) AS count FROM students WHERE teacher_id = ?", teacher_id
    )
    return render_template(
        "teacher_dashboard.html",
        role=session["user_role"],
        teacher=teacher[0],
        students=students[0]["count"],
    )


# Edit Profile Route


@app.route("/edit_admin_profile", methods=["GET", "POST"])
@login_required
def edit_admin_profile():
    admin_id = session.get("user_id")
    if admin_id is None:
        return render_template("message.html", msg="Unauthorized Access")

    if request.method == "POST":
        input_values = {
            "firstname": request.form.get("firstname"),
            "lastname": request.form.get("lastname"),
            "email": request.form.get("email"),
            "institute": request.form.get("institute"),
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "confirmation": request.form.get("confirmation"),
        }

        # Check if all fields are filled and handle password confirmation
        if (
            not all(input_values.values())
            or input_values["password"] != input_values["confirmation"]
        ):
            return render_template(
                "message.html",
                msg="Please fill in all fields and ensure password confirmation matches.",
            )

        # Check if the username is already taken (excluding the current admin)
        existing_user = db.execute(
            "SELECT id FROM admins WHERE username = ? AND id != ?",
            input_values["username"],
            admin_id,
        )

        if len(existing_user) > 0:
            return render_template(
                "message.html",
                msg="Username is already taken. Please choose a different one.",
            )

        try:
            # Update the admin's profile in the database
            db.execute(
                "UPDATE admins SET firstname = ?, lastname = ?, email = ?, institute = ?, username = ?, password = ? WHERE id = ?",
                input_values["firstname"],
                input_values["lastname"],
                input_values["email"],
                input_values["institute"],
                input_values["username"],
                generate_password_hash(input_values["password"]),
                admin_id,
            )
            return redirect("/profile")
        except Exception as e:
            print(f"Error during registration: {str(e)}")
            return render_template(
                "message.html",
                msg="An error occurred during editing profile. Please try again later.",
            )

    # Fetch and display the admin's data for editing
    admin_data = db.execute("SELECT * FROM admins WHERE id = ?", admin_id)
    if not admin_data:
        return render_template("message.html", msg="Admin Not Found")

    return render_template("edit_admin_profile.html", admin=admin_data[0])


@app.route("/edit_teacher_profile", methods=["GET", "POST"])
@login_required
def edit_teacher_profile():
    teacher_Id = request.args.get("teacher_id")
    if teacher_Id:
        Teacher_id = teacher_Id
        teacher_data = db.execute("SELECT * FROM teachers where id = ?", Teacher_id)
    if request.method == "POST":
        admin_id = session["user_id"]
        input_values = {
            "firstname": request.form.get("firstname"),
            "lastname": request.form.get("lastname"),
            "email": request.form.get("email"),
            "subject": request.form.get("subject"),
            "qualification": request.form.get("qualification"),
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "confirmation": request.form.get("confirmation"),
            "id": request.form.get("user_id"),
        }
        print("id")
        print(input_values["id"])
        # Check if all fields are empty or contain only whitespace
        all_fields_empty = all(
            value is None or value.strip() == "" for value in input_values.values()
        )
        if all_fields_empty:
            return render_template("message.html", msg="All fields must be filled")
        elif input_values["password"] != input_values["confirmation"]:
            return render_template(
                "message.html", msg="Password does not match with confirm password"
            )

        try:
            # Check if there is a user with the same username (excluding the current user)
            user = db.execute(
                "SELECT username FROM teachers WHERE id != ?", input_values["id"]
            )

            if user and user[0]["username"] == input_values["username"]:
                # Username is already taken by another user; return an error message
                return render_template(
                    "message.html",
                    msg="Username is already taken, choose a different one.",
                )
            db.execute(
                "UPDATE teachers SET firstname = ?, lastname = ?, email = ?, subject = ?, qualification = ?, username = ?, password = ? WHERE id = ?",
                input_values["firstname"],
                input_values["lastname"],
                input_values["email"],
                input_values["subject"],
                input_values["qualification"],
                input_values["username"],
                generate_password_hash(input_values["password"]),
                input_values["id"],
            )

            return redirect("/teachers")

        except Exception as e:
            print(f"Error during edit profile: {str(e)}")
            return render_template(
                "message.html",
                msg="An error occurred during editing profile. Please try again later.",
            )

    return render_template(
        "edit_teacher_profile.html", teacher=teacher_data[0], id=teacher_Id
    )


@app.route("/edit_student_profile", methods=["GET", "POST"])
@login_required
def edit_student_profile():
    student_Id = request.args.get("student_id")
    if student_Id:
        Student_id = student_Id
        student_data = db.execute("SELECT * FROM students where id = ?", Student_id)
    if request.method == "POST":
        admin_id = session["user_id"]
        input_values = {
            "firstname": request.form.get("firstname"),
            "lastname": request.form.get("lastname"),
            "email": request.form.get("email"),
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "confirmation": request.form.get("confirmation"),
            "id": request.form.get("user_id"),
        }
        # Check if all fields are empty or contain only whitespace
        all_fields_empty = all(
            value is None or value.strip() == "" for value in input_values.values()
        )
        if all_fields_empty:
            return render_template("message.html", msg="All fields must be filled")
        elif input_values["password"] != input_values["confirmation"]:
            return render_template(
                "message.html", msg="Password does not match with confirm password"
            )

        try:
            # Check if there is a user with the same username (excluding the current user)
            user = db.execute(
                "SELECT username FROM students WHERE id != ?", input_values["id"]
            )

            if user and user[0]["username"] == input_values["username"]:
                # Username is already taken by another user; return an error message
                return render_template(
                    "message.html",
                    msg="Username is already taken, choose a different one.",
                )
            db.execute(
                "UPDATE students SET firstname = ?, lastname = ?, email = ?, username = ?, password = ? WHERE id = ?",
                input_values["firstname"],
                input_values["lastname"],
                input_values["email"],
                input_values["username"],
                generate_password_hash(input_values["password"]),
                input_values["id"],
            )

            return redirect("/student_list")

        except Exception as e:
            print(f"Error during edit profile: {str(e)}")
            return render_template(
                "message.html",
                msg="An error occurred during editing profile. Please try again later.",
            )

    return render_template(
        "edit_student_profile.html", student=student_data[0], id=student_Id
    )


# Delete User Routes

@app.route("/delete_admin", methods=["GET", "POST"])
@login_required
def delete_admin():
    if request.method == "POST":
        user_id = session["user_id"]
        courses = db.execute("select * FROM courses WHERE admin_id = ?", user_id)
        students = db.execute("select * FROM students WHERE admin_id = ?", user_id)
        teachers = db.execute("select * FROM teachers WHERE admin_id = ?", user_id)
        if students or teachers or courses:
            return render_template(
                "message.html",
                msg="This profile cannot be deleted, you need to delete all of your classes, teachers and students first",
            )
        db.execute("DELETE FROM admins WHERE id = ?", user_id)
        return redirect("/logout")
    else:
        return redirect("/profile")


@app.route("/delete_class", methods=["GET", "POST"])
@login_required
def delete_class():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        students = db.execute("select * FROM students WHERE course_id = ?", user_id)
        teachers = db.execute("select * FROM teachers WHERE course_id = ?", user_id)
        if students or teachers:
            return render_template(
                "message.html",
                msg="This class cannot be deleted, you need to delete all of its teachers and students first!",
            )
        db.execute("DELETE FROM courses WHERE id = ?", user_id)
        return redirect("/classes")
    else:
        return redirect("/classes")

@app.route("/delete_teacher", methods=["GET", "POST"])
@login_required
def delete_teacher():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        students = db.execute("select * FROM students WHERE teacher_id = ?", user_id)
        if students:
            return render_template(
                "message.html",
                msg="This teacher cannot be deleted, you need to delete its students first!",
            )
        db.execute("DELETE FROM teachers WHERE id = ?", user_id)
        return redirect("/teachers")
    else:
        return redirect("/teachers")

@app.route("/delete_student", methods=["GET", "POST"])
@login_required
def delete_student():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        db.execute("DELETE FROM attendance WHERE student_id = ?", user_id)
        db.execute("DELETE FROM students WHERE id = ?", user_id)
        return redirect("/student_list")
    else:
        return redirect("/student_list")

